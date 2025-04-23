from openai import OpenAI
from typing import Callable, Optional

def create_openai_client(
    api_key: str,
    base_url: str = "https://api.groq.com/openai/v1",
    model: str = "mixtral-8x7b-32768"
) -> Callable[[str, Optional[str]], str]:
    """
    Returns a callable that sends prompts to an OpenAI-compatible LLM API
    using the new OpenAI Python SDK (v1+).
    """
    client = OpenAI(api_key=api_key, base_url=base_url)

    def call(prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[llm_call] Error calling Groq: {e}")
            return ""

    return call
