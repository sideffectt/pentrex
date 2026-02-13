"""LLM provider wrapper. Supports Anthropic, OpenAI, Ollama via LiteLLM."""

import anthropic
from pentrex.config import Config


class LLM:
    """Wrapper around Anthropic API. Swap to LiteLLM for multi-provider."""

    def __init__(self, config: Config):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.api_key)

    def chat(self, messages: list, system: str = "", tools: list = None) -> dict:
        kwargs = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = tools

        response = self.client.messages.create(**kwargs)
        return response

    def simple(self, prompt: str, system: str = "") -> str:
        """Single-turn completion, no tools."""
        resp = self.chat(
            messages=[{"role": "user", "content": prompt}],
            system=system,
        )
        return resp.content[0].text if resp.content else ""
