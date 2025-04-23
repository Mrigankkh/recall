from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid

@dataclass
class MemoryEntry:
    user_id: str
    content: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_accessed: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)
    importance: float = 0.5
    ttl_days: int = 365
    source: str = "unknown"
    embedding: Optional[List[float]] = None


    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "tags": self.tags,
            "importance": self.importance,
            "ttl_days": self.ttl_days,
            "source": self.source,
            "embedding": self.embedding,
        }

    @staticmethod
    def from_dict(data: dict) -> 'MemoryEntry':
        return MemoryEntry(
            id=data.get("id", str(uuid.uuid4())),
            user_id=data["user_id"],
            content=data["content"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_accessed=datetime.fromisoformat(data["last_accessed"]),
            tags=data.get("tags", []),
            importance=data.get("importance", 0.5),
            ttl_days=data.get("ttl_days", 365),
            source=data.get("source", "unknown"),
            embedding=data.get("embedding"),
        )
