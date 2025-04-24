from collections import defaultdict
from .extractor import extract_memories_from_input

_batch_cache = defaultdict(list)

def extract_from_batch(user_id, message, store, llm_call, metadata=None):
    batch_size = metadata.get("batch_size", 5) if metadata else 5

    _batch_cache[user_id].append(message)

    if len(_batch_cache[user_id]) < batch_size:
        return [] 

    # Concatenate batch for extraction
    combined_input = "\n".join(_batch_cache[user_id])
    extracted = extract_memories_from_input(combined_input, llm_call)

    # Reset batch
    _batch_cache[user_id] = []

    return extracted
def is_memory_worthy(text: str) -> bool:
    # TODO: Implement a more sophisticated heuristic
    return len(text) > 25 or any(word in text.lower() for word in ["i", "my", "remember"])
