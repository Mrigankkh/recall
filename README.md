# Recall SDK

[![PyPI version](https://img.shields.io/pypi/v/recall-sdk)](https://pypi.org/project/recall-sdk/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

Recall is a pluggable memory layer for LLM applications. It enables long-term memory by extracting, storing, and retrieving relevant information from user input, and injecting it back into prompts. Compatible with any OpenAI-style API.

---

## Overview

Recall SDK gives your LLM apps long-term memory. It:
- Extracts memory-worthy facts from user input
- Stores them with TTL, tags, importance, and source
- Injects relevant context into future prompts

It works with any OpenAI-compatible LLM API (OpenAI, Groq, etc.).

---

## Installation

```bash
pip install recall-sdk

```

## Quickstart

```python
from recall import withrecall
from recall.memory import MemoryStore
from recall.llm.llm_client import create_openai_client

llm = create_openai_client(
    api_key="your-key",
    base_url="https://api.groq.com/openai/v1",
    model="mixtral-8x7b-32768"
)

store = MemoryStore()

with_recall = withrecall(llm=llm, store=store)
response = with_recall.chat("My dog's name is Ollie.")
print(response)

with_recall.remember("I live in Berlin.", tags=["location"], importance=0.8)
```
## High Level API: withrecall()

### Contructor
```python
with_recall = withrecall(
    llm,                 # Callable that takes prompt and optional system_prompt
    store,               # MemoryStore instance
    user_id="default",   # Optional session/user ID
    strategy="always",   # Extraction strategy: always, batch
    metadata=None        # Optional metadata passed to handler
)
```

### Methods
```python 
with_recall.chat(message: str) -> str
```
Extracts memory, injects relevant context, returns LLM response.
```python
chat.remember(content: str, tags: List[str] = [], importance: float = 0.5)
```
Manually store memory entries.

## Low-Level API (for more granular control over the memory)
### Memory Store
```python
from recall.memory import MemoryStore

store = MemoryStore()

store.add_memory(MemoryEntry(...))
store.get_memories("user-id")
store.export_memories("user-id", path="backup.json")
store.import_memories(data)
```
### Memory Entry
```python
from recall.memory import MemoryEntry

MemoryEntry(
    user_id="user-id",
    content="The Eiffel Tower is in Paris.",
    tags=["travel"],
    importance=0.9
)

```

## Extraction Strategies
- "always" : Extract memory from every message sent by the user [an extra LLM call to create a memory from the user's prompt and store it in the Memory]
- "batch" : Extract memory every N messages [meta data controlled] [an extra LLM call after every N messages. This call uses all previous user prompts to get MemoryEntries]
- "heuristic" : TBD

## Memory Structure
Memory Structure
Each memory is stored with:
- id (UUID)
- user_id
- content
- created_at
- last_accessed
- tags (list of strings)
- importance (float 0–1)
- ttl_days (time to live)
- source (chatbot, manual, etc.)
- embedding (To be integrated with high level API in future for semantic search)

