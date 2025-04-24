import os
from recall.withrecall import withrecall
from recall.memory.memory_store import MemoryStore
from recall.llm.llm_client import create_openai_client
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv() # === Load from environment ===


api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

if not api_key:
    raise ValueError("Missing OPENAI_API_KEY in environment variables.")

# === Setup LLM client and memory store ===
llm = create_openai_client(api_key=api_key, base_url=base_url, model=model)
store = MemoryStore()

# === withrecall session ===
chat = withrecall(llm=llm, store=store, user_id="manual-test-user")

print("🧠 withrecall() manual test. Type 'exit' to quit.")
print("You can also type 'mem' to print current memories.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("👋 Exiting...")
        break

    elif user_input.lower() == "mem":
        print("\n[🔎 Memory contents]")
        memories = store.get_memories("manual-test-user")
        for m in memories:
            print(f"- {m.content} (tags: {m.tags}, importance: {m.importance})")
        print()
        continue

    response = chat.chat(user_input)
    print("🤖", response, "\n")
