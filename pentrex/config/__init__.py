"""Pentrex configuration."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    api_key: str = ""
    model: str = "claude-haiku-4-5-20251001"
    max_tokens: int = 4096
    max_agent_iterations: int = 25
    target: str = ""
    docker_mode: bool = False
    allowed_tools: list = field(default_factory=lambda: [
        "terminal", "nmap_scan", "save_note", "read_notes", "quiz", "explain"
    ])

    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        env_model = os.getenv("PENTREX_MODEL")
        if env_model:
            self.model = env_model

    @classmethod
    def from_env(cls) -> "Config":
        return cls()


# Safety constants
BLOCKED_COMMANDS = [
    "rm -rf /", "mkfs", "dd if=/dev/zero",
    ":(){ :|:& };:", "chmod -R 777 /",
]

MAX_COMMAND_TIMEOUT = 120  # seconds
