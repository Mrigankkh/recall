import sqlite3
import json
from datetime import datetime
import numpy as np
from typing import List, Optional
from .memory_entry import MemoryEntry

class MemoryStore:
    def __init__(self, db_path: str = "recall.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                content TEXT,
                created_at TEXT,
                last_accessed TEXT,
                tags TEXT,
                importance REAL,
                ttl_days INTEGER,
                source TEXT,
                embedding TEXT
            )
        ''')
        self.conn.commit()

    def add_memory(self, memory: MemoryEntry):
        self.conn.execute('''
            INSERT OR REPLACE INTO memories (
                id, user_id, content, created_at, last_accessed,
                tags, importance, ttl_days, source, embedding
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory.id,
            memory.user_id,
            memory.content,
            memory.created_at.isoformat(),
            memory.last_accessed.isoformat(),
            json.dumps(memory.tags),
            memory.importance,
            memory.ttl_days,
            memory.source,
            json.dumps(memory.embedding) if memory.embedding else None
        ))
        self.conn.commit()
        
    def get_memories(self, user_id: str) -> List[MemoryEntry]:
        cursor = self.conn.execute('''
            SELECT * FROM memories WHERE user_id = ?
        ''', (user_id,))
        rows = cursor.fetchall()

        memories = []
        for row in rows:
            self._update_last_accessed(row[0])  # update timestamp
            memory = self._row_to_memory(row)
            memories.append(memory)

        return memories


    def delete_memory(self, memory_id: str):
        self.conn.execute('''
            DELETE FROM memories WHERE id = ?
        ''', (memory_id,))
        self.conn.commit()

    def _row_to_memory(self, row) -> MemoryEntry:
        return MemoryEntry(
            id=row[0],
            user_id=row[1],
            content=row[2],
            created_at=datetime.fromisoformat(row[3]),
            last_accessed=datetime.fromisoformat(row[4]),
            tags=json.loads(row[5]),
            importance=row[6],
            ttl_days=row[7],
            source=row[8],
            embedding=json.loads(row[9]) if row[9] else None
        )
        
    def search_memories(self, user_id: str, tags: Optional[List[str]] = None, min_importance: float = 0.0) -> List[MemoryEntry]:
        query = 'SELECT * FROM memories WHERE user_id = ?'
        params = [user_id]

        if tags:
            query += ' AND (' + ' OR '.join(['tags LIKE ?' for _ in tags]) + ')'
            params.extend([f'%{tag}%' for tag in tags])

        if min_importance > 0.0:
            query += ' AND importance >= ?'
            params.append(min_importance)

        cursor = self.conn.execute(query, tuple(params))
        rows = cursor.fetchall()

        memories = []
        for row in rows:
            self._update_last_accessed(row[0])  # <-- Add this line
            memory = self._row_to_memory(row)
            memories.append(memory)

        return memories

    def semantic_search(self, user_id: str, query_embedding: List[float], top_k: int = 5) -> List[MemoryEntry]:
        cursor = self.conn.execute('SELECT * FROM memories WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        memories = []

        for row in rows:
            embedding = json.loads(row[9]) if row[9] else None
            if embedding:
                similarity = self._cosine_similarity(query_embedding, embedding)
                memories.append((similarity, self._row_to_memory(row)))

        # Sort by similarity in descending order
        memories.sort(key=lambda x: x[0], reverse=True)
        return [memory for _, memory in memories[:top_k]]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
            return 0.0
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    
    def remove_expired_memories(self):
        now = datetime.utcnow()
        cursor = self.conn.execute('SELECT id, created_at, ttl_days FROM memories')
        rows = cursor.fetchall()
        for row in rows:
            created_at = datetime.fromisoformat(row[1])
            ttl = row[2]
            if (now - created_at).days > ttl:
                self.delete_memory(row[0])
                
    def _update_last_accessed(self, memory_id: str):
        self.conn.execute(
            "UPDATE memories SET last_accessed = ? WHERE id = ?",
            (datetime.utcnow().isoformat(), memory_id)
        )
        self.conn.commit()
        
    def cap_memory(self, user_id: str, max_entries: int):
        cursor = self.conn.execute('''
            SELECT id FROM memories
            WHERE user_id = ?
            ORDER BY importance ASC, created_at ASC
        ''', (user_id,))
        rows = cursor.fetchall()
        if len(rows) > max_entries:
            to_delete = rows[:len(rows) - max_entries]
            for row in to_delete:
                self.delete_memory(row[0])