"""Terminal tool - execute shell commands with safety checks."""

import subprocess
import shlex
from pentrex.tools.registry import register
from pentrex.config import BLOCKED_COMMANDS, MAX_COMMAND_TIMEOUT


def _is_safe(command: str) -> bool:
    """Block dangerous commands."""
    cmd_lower = command.lower().strip()
    for blocked in BLOCKED_COMMANDS:
        if blocked in cmd_lower:
            return False
    return True


@register(
    name="terminal",
    description="Execute a shell command and return output. Use for running pentest tools like nmap, nikto, gobuster, curl, etc. Only use on authorized targets.",
    parameters={
        "command": {
            "type": "string",
            "description": "Shell command to execute"
        }
    },
)
def terminal(command: str) -> dict:
    if not _is_safe(command):
        return {"error": "Command blocked for safety reasons."}

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=MAX_COMMAND_TIMEOUT,
        )
        output = result.stdout
        if result.stderr:
            output += f"\n[stderr] {result.stderr}"

        # Truncate very long output
        if len(output) > 8000:
            output = output[:4000] + "\n\n... [truncated] ...\n\n" + output[-2000:]

        return {
            "command": command,
            "exit_code": result.returncode,
            "output": output or "(no output)",
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Command timed out after {MAX_COMMAND_TIMEOUT}s"}
    except Exception as e:
        return {"error": str(e)}
