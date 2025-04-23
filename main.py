from memory.memory_store import MemoryStore
from llm.llm_client import create_openai_client
from handlers.user_message_handler import handle_user_message

# Then pass it into extract_memories_from_input()

from typing import Callable, Dict, List
import json

llm_call = create_openai_client(
    api_key="sk-...",
    base_url="https://openrouter.ai/api/v1",  
    model="gpt-3.5-turbo"
)

store = MemoryStore()
user_input = "I love jazz music and I’m planning a trip to Paris."

handle_user_message("user-123", user_input, store, llm_call)