from ..memory.memory_entry import MemoryEntry
from ..memory.memory_store import MemoryStore
from ..llm.extractor import extract_memories_from_input

# Then pass it into extract_memories_from_input()

from typing import Callable, Dict, List
import json


def handle_user_message(user_id: str, message: str, store: MemoryStore, llm_call: Callable[[str], str]):
    extracted_memories = extract_memories_from_input(message, llm_call)

    for mem in extracted_memories:
        entry = MemoryEntry(
            user_id=user_id,
            content=mem["content"],
            tags=mem["tags"],
            importance=mem["importance"]
        )
        store.add_memory(entry)
