from memory.memory_store import MemoryStore
from llm.llm_client import create_openai_client
from llm.extractor import extract_memories_from_input
from llm.prompt_serializer import serialize_for_openai
from handlers.user_message_handler import handle_user_message

import os
from dotenv import load_dotenv

load_dotenv()

# === Setup ===
user_id = "demo-user"
store = MemoryStore()

llm_call = create_openai_client(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
)

print("🧠 Recall Memory Chat Demo")
print("Type 'exit' to quit.\n")

# === Chat Loop ===
while True:
    user_input = input("You: ")

    if user_input.lower() in {"exit", "quit"}:
        print("👋 Goodbye!")
        break

    # 1. Extract + store new memory
    handle_user_message(user_id, user_input, store, llm_call)

    # 2. Retrieve relevant memories
    memories = store.search_memories(user_id, min_importance=0.4)

    # 3. Inject into prompt
    system_prompt = serialize_for_openai(memories)

    # 4. Get LLM reply
    response = llm_call(prompt=user_input, system_prompt=system_prompt)

    print("🤖", response)
