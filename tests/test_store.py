import pytest
import json
from recall.memory.memory_store import MemoryStore
from recall.memory.memory_entry import MemoryEntry
from datetime import datetime, timezone, timedelta

@pytest.fixture(scope="function")
def store():
    return MemoryStore(db_path=":memory:")

def test_add_and_get_memory(store):
    entry = MemoryEntry(user_id="user1", content="Hello!")
    store.add_memory(entry)
    memories = store.get_memories("user1")
    assert len(memories) == 1
    assert memories[0].content == "Hello!"

def test_delete_memory(store):
    entry = MemoryEntry(user_id="user1", content="To be deleted")
    store.add_memory(entry)
    store.delete_memory(entry.id)
    memories = store.get_memories("user1")
    assert len(memories) == 0

def test_search_by_tag(store):
    entry = MemoryEntry(user_id="u1", content="Testing tags", tags=["tag1"])
    store.add_memory(entry)
    results = store.search_memories("u1", tags=["tag1"])
    assert len(results) == 1
    assert "tag1" in results[0].tags

def test_search_by_importance(store):
    entry1 = MemoryEntry(user_id="u2", content="Low importance", importance=0.1)
    entry2 = MemoryEntry(user_id="u2", content="High importance", importance=0.9)
    store.add_memory(entry1)
    store.add_memory(entry2)
    results = store.search_memories("u2", min_importance=0.5)
    assert len(results) == 1
    assert results[0].importance == 0.9

# def test_export_and_import(store):
#     entry = MemoryEntry(user_id="userX", content="Export me!", tags=["x"])
#     store.add_memory(entry)
    
#     data = store.export_memories("userX")
#     assert len(data) == 1  # Sanity check

#     assert isinstance(data, list)
#     store.clear_user_memories("userX")
#     assert len(store.get_memories("userX")) == 0
#     print("EXPORTED DATA:", json.dumps(data, indent=2))

#     store.import_memories(data)
#     assert len(store.get_memories("userX")) == 1
#     assert store.get_memories("userX")[0].content == "Export me!"
    
def test_export_and_import(store):
    print("\n---- START TEST ----")
    
    entry = MemoryEntry(user_id="userX", content="Export me!", tags=["x"])
    print("[DEBUG] ENTRY:", entry.to_dict())
    
    store.add_memory(entry)
    print("[DEBUG] GET AFTER ADD:", [m.to_dict() for m in store.get_memories("userX")])
    
    data = store.export_memories("userX")
    print("[DEBUG] EXPORTED DATA:", data)

    assert len(data) == 1  

    store.clear_user_memories("userX")
    print("[DEBUG] GET AFTER CLEAR:", store.get_memories("userX"))

    store.import_memories(data)
    print("[DEBUG] GET AFTER IMPORT:", [m.to_dict() for m in store.get_memories("userX")])

    assert len(store.get_memories("userX")) == 1
    assert store.get_memories("userX")[0].content == "Export me!"


def test_expired_memory_removal(store):
    old_date = datetime.now(timezone.utc) - timedelta(days=400)
    expired_entry = MemoryEntry(user_id="userZ", content="Old one", created_at=old_date, ttl_days=30)
    fresh_entry = MemoryEntry(user_id="userZ", content="Fresh one")
    store.add_memory(expired_entry)
    store.add_memory(fresh_entry)
    store.remove_expired_memories()
    remaining = store.get_memories("userZ")
    assert len(remaining) == 1
    assert remaining[0].content == "Fresh one"