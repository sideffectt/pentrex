import os
from dataclasses import dataclass
from pathlib import Path

# Load .env file manually (no dotenv dependency needed)
def load_env():
    env_paths = [
        Path(".env"),
        Path(__file__).parent.parent / ".env",
        Path(__file__).parent.parent.parent / ".env",
    ]
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip()
            break

load_env()


@dataclass
class Config:
    api_key: str = ""
    model: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 4096
    max_iterations: int = 10

    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
