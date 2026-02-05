"""
Pentrex agent loop.
Handles tool calls and conversation flow.
"""

import json
import anthropic

from pentrex.config import Config
from pentrex.tools import get_all_tools, run_tool
from pentrex.knowledge.prompt import SYSTEM_PROMPT


class Agent:
    def __init__(self, config: Config):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.api_key)
        self.history = []

    def chat(self, message: str) -> str:
        self.history.append({"role": "user", "content": message})

        for _ in range(self.config.max_iterations):
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                system=SYSTEM_PROMPT,
                tools=get_all_tools(),
                messages=self.history,
            )

            if response.stop_reason == "tool_use":
                self.history.append({
                    "role": "assistant",
                    "content": self._serialize(response.content)
                })

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = run_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result, ensure_ascii=False)
                        })

                self.history.append({"role": "user", "content": tool_results})
                continue

            # Done
            text = "".join(b.text for b in response.content if hasattr(b, "text"))
            self.history.append({"role": "assistant", "content": text})
            return text

        return "Max iterations reached."

    def reset(self):
        self.history = []

    def _serialize(self, content):
        out = []
        for b in content:
            if b.type == "text":
                out.append({"type": "text", "text": b.text})
            elif b.type == "tool_use":
                out.append({
                    "type": "tool_use",
                    "id": b.id,
                    "name": b.name,
                    "input": b.input
                })
        return out
