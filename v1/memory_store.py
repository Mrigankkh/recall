from typing import List, Dict
from memory.memory_entry import MemoryEntry

class MemoryStore:
    def __init__(self):
        self.store: Dict[str, List[MemoryEntry]] = {}

    def add_memory(self, memory: MemoryEntry):
        if memory.user_id not in self.store:
            self.store[memory.user_id] = []
        self.store[memory.user_id].append(memory)

    def get_memories(self, user_id: str) -> List[MemoryEntry]:
        return self.store.get(user_id, [])

    def delete_memory(self, user_id: str, memory_id: str):
        if user_id in self.store:
            self.store[user_id] = [
                mem for mem in self.store[user_id] if mem.id != memory_id
            ]
