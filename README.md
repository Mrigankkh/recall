# Recall

[![PyPI version](https://img.shields.io/pypi/v/recall-sdk)](https://pypi.org/project/recall-sdk/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

Recall is a pluggable memory layer for LLM applications. It enables long-term memory by extracting, storing, and retrieving relevant information from user input, and injecting it back into prompts. Compatible with any OpenAI-style API such as OpenAI, Groq, Together.ai, and OpenRouter.

---

## Installation

```bash
pip install recall-sdk
```
For development:

```bash
git clone https://github.com/yourusername/recall
cd recall
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Quickstart

```python
from recall import MemoryStore, handle_user_message, serialize_for_openai
from openai import OpenAI

# Initialize your LLM client (OpenAI, Groq, etc.)
client = OpenAI(api_key="sk-...")

def llm_call(prompt, system_prompt=None):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(model="gpt-4", messages=messages)
    return response.choices[0].message.content.strip()

# Memory setup
store = MemoryStore()
user_id = "user-001"

# Extract and store memory from user input
handle_user_message(user_id, "I'm allergic to peanuts", store, llm_call)

# Retrieve and inject memory into prompt
memories = store.search_memories(user_id, min_importance=0.4)
system_prompt = serialize_for_openai(memories)

# Generate response with context
response = llm_call("What should I eat?", system_prompt)
print(response)
```

## Features
Automatic memory extraction from user input using an LLM

Persistent memory store with TTL, importance, tags, and embeddings

Relevance-based memory search and filtering

Prompt injection for OpenAI-compatible APIs

Works with any model that supports OpenAI's chat API format