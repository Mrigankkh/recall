from recall.memory import MemoryStore
from recall.handlers import handle_user_message
from recall.llm.prompt_serializer import serialize_for_openai

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

def withrecall(llm, store, user_id="default", strategy="always", metadata=None) -> WithRecallSession:
    return WithRecallSession(llm, store, user_id, strategy, metadata)
