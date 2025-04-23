import pytest
from datetime import datetime, timezone
from recall.memory.memory_entry import MemoryEntry

def test_to_dict_round_trip():
    entry = MemoryEntry(
        user_id="user1",
        content="This is a test.",
        tags=["test", "note"],
        importance=0.9,
        ttl_days=30,
        source="unit-test",
        embedding=[0.1, 0.2, 0.3]
    )

    data = entry.to_dict()
    restored = MemoryEntry.from_dict(data)

    assert restored.user_id == entry.user_id
    assert restored.content == entry.content
    assert restored.tags == entry.tags
    assert restored.importance == entry.importance
    assert restored.ttl_days == entry.ttl_days
    assert restored.source == entry.source
    assert restored.embedding == entry.embedding

def test_default_values():
    entry = MemoryEntry(user_id="u1", content="Hello world")
    assert entry.importance == 0.5
    assert entry.ttl_days == 365
    assert entry.source == "unknown"
    assert isinstance(entry.created_at, datetime)
    assert isinstance(entry.last_accessed, datetime)

def test_missing_optional_fields_in_dict():
    now = datetime.now(timezone.utc).isoformat()
    minimal_data = {
        "id": "abc-123",
        "user_id": "user123",
        "content": "Just testing.",
        "created_at": now,
    }

    restored = MemoryEntry.from_dict(minimal_data)
    assert restored.user_id == "user123"
    assert restored.tags == []
    assert restored.importance == 0.5
    assert restored.ttl_days == 365
    assert restored.source == "import"  
    assert restored.embedding is None