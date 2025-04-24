from typing import Callable, Dict, List
import json
import logging

def extract_memories_from_input(prompt: str, llm_call: Callable[[str], str]) -> List[Dict]:
    """
    Uses an LLM to extract memory-worthy entries from a user input.

    Args:
        prompt: The full user input text
        llm_call: A function that takes a string prompt and returns a string response (expected to be JSON)

    Returns:
        List of memory entries in dict form
    """
    extraction_prompt = (
        "Extract memory-worthy facts from the user input below. "
        "Respond with a JSON list of dicts like: "
        "[{\"content\": \"...\", \"tags\": [\"...\"], \"importance\": 0.0 - 1.0}].\n\n"
        f"User input:\n{prompt}"
    )

    response_text = llm_call(extraction_prompt)
    try:
        return json.loads(response_text)
    except Exception as e:
        logging.basicConfig(level=logging.ERROR)  
        logger = logging.getLogger(__name__)
        logger.info(f"[extract_memories_from_input] Failed to parse LLM response: {e}")
        return []
