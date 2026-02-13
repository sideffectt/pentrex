"""Nmap scanning tool with common scan profiles."""

import subprocess
import shutil
from pentrex.tools.registry import register
from pentrex.config import MAX_COMMAND_TIMEOUT

SCAN_PROFILES = {
    "quick": "-sV -T4 --top-ports 100",
    "full": "-sV -sC -p- -T4",
    "stealth": "-sS -T2 -f",
    "udp": "-sU --top-ports 50 -T4",
    "vuln": "-sV --script vuln -T4",
    "os": "-O -sV -T4",
}


@register(
    name="nmap_scan",
    description="Run an nmap scan against a target. Profiles: quick, full, stealth, udp, vuln, os. Or provide custom flags.",
    parameters={
        "target": {
            "type": "string",
            "description": "Target IP, hostname, or CIDR range"
        },
        "profile": {
            "type": "string",
            "description": "Scan profile: quick, full, stealth, udp, vuln, os. Default: quick"
        },
        "flags": {
            "type": "string",
            "description": "Custom nmap flags (overrides profile)"
        },
    },
    required=["target"],
)
def nmap_scan(target: str, profile: str = "quick", flags: str = "") -> dict:
    if not shutil.which("nmap"):
        return {"error": "nmap not installed. Install with: sudo apt install nmap"}

    scan_flags = flags if flags else SCAN_PROFILES.get(profile, SCAN_PROFILES["quick"])
    cmd = f"nmap {scan_flags} {target}"

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=MAX_COMMAND_TIMEOUT,
        )
        output = result.stdout
        if len(output) > 8000:
            output = output[:4000] + "\n... [truncated] ...\n" + output[-2000:]

        return {
            "command": cmd,
            "profile": profile,
            "output": output or "(no output)",
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Scan timed out after {MAX_COMMAND_TIMEOUT}s"}
    except Exception as e:
        return {"error": str(e)}
