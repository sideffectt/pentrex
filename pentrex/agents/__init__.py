"""Pentrex agent implementations."""

import json
from pentrex.config import Config
from pentrex.llm import LLM
from pentrex.tools import get_all_tools, run_tool
from pentrex.tools.notes import _load_notes
from pentrex.knowledge.prompts import build_system_prompt

# Re-export Crew
from pentrex.agents.crew import Crew


class AssistAgent:
    """Interactive chat agent — user controls the flow."""

    def __init__(self, config: Config):
        self.config = config
        self.llm = LLM(config)
        self.history: list = []
        self.target = config.target

    def set_target(self, target: str):
        self.target = target

    def chat(self, message: str) -> str:
        self.history.append({"role": "user", "content": message})

        notes = _load_notes()
        system = build_system_prompt(
            mode="assist", target=self.target, notes=notes,
        )
        tools = get_all_tools()

        # Agent loop — handle tool calls
        for _ in range(self.config.max_agent_iterations):
            response = self.llm.chat(
                messages=self.history,
                system=system,
                tools=tools,
            )

            # Check if response has tool use
            has_tool_use = any(b.type == "tool_use" for b in response.content)

            if not has_tool_use:
                # Pure text response
                text = "".join(b.text for b in response.content if b.type == "text")
                self.history.append({"role": "assistant", "content": self._serialize(response.content)})
                return text

            # Process tool calls
            self.history.append({"role": "assistant", "content": self._serialize(response.content)})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = run_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, default=str),
                    })

            self.history.append({"role": "user", "content": tool_results})

        return "Max iterations reached. Use /clear to reset."

    def reset(self):
        self.history = []

    def _serialize(self, content) -> list:
        out = []
        for b in content:
            if b.type == "text":
                out.append({"type": "text", "text": b.text})
            elif b.type == "tool_use":
                out.append({
                    "type": "tool_use",
                    "id": b.id,
                    "name": b.name,
                    "input": b.input,
                })
        return out


class AutoAgent:
    """Autonomous agent — executes a task independently."""

    def __init__(self, config: Config):
        self.config = config
        self.llm = LLM(config)
        self.target = config.target
        self._stopped = False

    def stop(self):
        self._stopped = True

    def run(self, task: str, on_step=None) -> str:
        """Run task autonomously. on_step callback for progress updates."""
        self._stopped = False
        history = []
        notes = _load_notes()

        system = build_system_prompt(
            mode="agent", target=self.target, task=task, notes=notes,
        )
        tools = get_all_tools()

        history.append({"role": "user", "content": f"Execute this task: {task}"})

        final_output = []

        for step in range(self.config.max_agent_iterations):
            if self._stopped:
                final_output.append("[Agent stopped by user]")
                break

            response = self.llm.chat(messages=history, system=system, tools=tools)

            has_tool_use = any(b.type == "tool_use" for b in response.content)

            # Collect text
            for b in response.content:
                if b.type == "text" and b.text.strip():
                    final_output.append(b.text)
                    if on_step:
                        on_step(f"[step {step+1}] {b.text[:100]}...")

            if not has_tool_use:
                break

            # Serialize and execute tools
            serialized = []
            for b in response.content:
                if b.type == "text":
                    serialized.append({"type": "text", "text": b.text})
                elif b.type == "tool_use":
                    serialized.append({"type": "tool_use", "id": b.id, "name": b.name, "input": b.input})
            history.append({"role": "assistant", "content": serialized})

            tool_results = []
            for b in response.content:
                if b.type == "tool_use":
                    if on_step:
                        on_step(f"[tool] {b.name}({json.dumps(b.input)[:80]})")
                    result = run_tool(b.name, b.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": b.id,
                        "content": json.dumps(result, default=str),
                    })

            history.append({"role": "user", "content": tool_results})

        return "\n\n".join(final_output) if final_output else "Task completed."
