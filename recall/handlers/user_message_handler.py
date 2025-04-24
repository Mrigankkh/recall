from ..memory.memory_entry import MemoryEntry
from ..memory.memory_store import MemoryStore
from ..llm.extractor import extract_memories_from_input
from ..constants import ExtractionStrategy

from typing import Callable, Dict, List, Optional
import json


def handle_user_message(
    user_id: str,
    message: str,
    store: MemoryStore,
    llm_call: Callable[[str], str],
    extraction_strategy: ExtractionStrategy = ExtractionStrategy.ALWAYS,
    metadata: Optional[dict] = None
):
    if isinstance(extraction_strategy, str):
        extraction_strategy = ExtractionStrategy.from_str(extraction_strategy)

    if extraction_strategy == ExtractionStrategy.ALWAYS:
        extracted_memories = extract_memories_from_input(message, llm_call)

    elif extraction_strategy == ExtractionStrategy.BATCH:
        from ..extraction.strategies import extract_from_batch
        extracted_memories = extract_from_batch(user_id, message, store, llm_call, metadata)

    elif extraction_strategy == ExtractionStrategy.HEURISTIC:
        from ..extraction.strategies import is_memory_worthy
        if is_memory_worthy(message):
            extracted_memories = extract_memories_from_input(message, llm_call)
        else:
            extracted_memories = []

    else:
        raise ValueError(f"Unsupported extraction strategy: {extraction_strategy}")

    for mem in extracted_memories:
        entry = MemoryEntry(
            user_id=user_id,
            content=mem["content"],
            tags=mem["tags"],
            importance=mem["importance"]
        )
        store.add_memory(entry)
