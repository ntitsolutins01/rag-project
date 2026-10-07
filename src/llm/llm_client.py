"""Cliente de LLM. Implementado com Claude (Anthropic); adicione OpenAI/Gemini aqui."""
import os

import anthropic


class LLMClient:
    def __init__(self, model: str, max_tokens: int = 1024, temperature: float = 0.2):
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def generate(self, system: str, user: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(b.text for b in response.content if b.type == "text")
