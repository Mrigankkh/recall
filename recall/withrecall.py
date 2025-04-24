from .memory.memory_entry import MemoryEntry
from .memory.memory_store import MemoryStore
from .handlers.user_message_handler import handle_user_message
from .llm.prompt_serializer import serialize_for_openai
from typing import Optional, List

class WithRecallSession:
    def __init__(self, llm, store: MemoryStore, user_id: str = "default", strategy="always", metadata=None):
        self.llm = llm
        self.store = store
        self.user_id = user_id
        self.strategy = strategy
        self.metadata = metadata or {}

    def chat(self, message: str) -> str:
        handle_user_message(
            user_id=self.user_id,
            message=message,
            store=self.store,
            llm_call=self.llm,
            extraction_strategy=self.strategy,
            metadata=self.metadata,
        )

        memories = self.store.search_memories(self.user_id, min_importance=0.4)
        system_prompt = serialize_for_openai(memories)
        return self.llm(prompt=message, system_prompt=system_prompt)

    def remember(
        self,
        content: str,
        tags: Optional[List[str]] = None,
        importance: float = 0.5,
        ttl_days: int = 365,
        source: str = "manual"
    ):
        entry = MemoryEntry(
            user_id=self.user_id,
            content=content,
            tags=tags or [],
            importance=importance,
            ttl_days=ttl_days,
            source=source
        )
        self.store.add_memory(entry)

def withrecall(llm, store, user_id="default", strategy="always", metadata=None) -> WithRecallSession:
    return WithRecallSession(llm, store, user_id, strategy, metadata)
