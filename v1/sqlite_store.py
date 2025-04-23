import sqlite3
import json
from datetime import datetime, timedelta
from typing import List
from memory.memory_entry import MemoryEntry

class MemoryStore:
    def __init__(self, db_path: str = "recall_memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
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
        """)
        self.conn.commit()

    def add_memory(self, memory: MemoryEntry):
        self.conn.execute("""
        INSERT OR REPLACE INTO memory (
            id, user_id, content, created_at, last_accessed,
            tags, importance, ttl_days, source, embedding
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
        cursor = self.conn.execute("SELECT * FROM memory WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        return [self._row_to_memory(row) for row in rows]

    def delete_memory(self, memory_id: str):
        self.conn.execute("DELETE FROM memory WHERE id = ?", (memory_id,))
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
