from typing import List
from ..memory.memory_entry import MemoryEntry

def serialize_for_openai(memories: List[MemoryEntry]) -> str:
    """
    Converts a list of MemoryEntry objects into a system prompt string
    for injection into an OpenAI-compatible chat model.
    """
    if not memories:
        return "The user has no known memory yet."

    # Sort by importance and recency
    sorted_memories = sorted(
        memories,
        key=lambda m: (m.importance, m.last_accessed),
        reverse=True
    )

    lines = ["The user previously mentioned:"]
    for mem in sorted_memories:
        lines.append(f"- {mem.content}")

    return "\n".join(lines)
