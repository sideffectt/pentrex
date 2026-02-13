"""Pentrex Terminal User Interface."""

import sys
import json
import signal

from pentrex.config import Config
from pentrex.agents import AssistAgent, AutoAgent
from pentrex.tools import get_tool_names
from pentrex.tools.notes import _load_notes
from pentrex.playbooks import list_playbooks, build_playbook_task
from pentrex.mcp import list_mcp_servers, add_mcp_server
from pentrex.runtime.report import generate_report, save_report


# ANSI colors
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


BANNER = f"""
{C.CYAN}{C.BOLD}
    ██████╗ ███████╗███╗   ██╗████████╗██████╗ ███████╗██╗  ██╗
    ██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██╔══██╗██╔════╝╚██╗██╔╝
    ██████╔╝█████╗  ██╔██╗ ██║   ██║   ██████╔╝█████╗   ╚███╔╝
    ██╔═══╝ ██╔══╝  ██║╚██╗██║   ██║   ██╔══██╗██╔══╝   ██╔██╗
    ██║     ███████╗██║ ╚████║   ██║   ██║  ██║███████╗██╔╝ ██╗
    ╚═╝     ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{C.RESET}
    {C.DIM}AI Penetration Testing Agent v2.0{C.RESET}
    {C.DIM}Type /help for commands • /quit to exit{C.RESET}
"""

HELP_TEXT = f"""
  {C.YELLOW}{C.BOLD}Commands:{C.RESET}
    {C.GREEN}/agent <task>{C.RESET}     Run autonomous agent on task
    {C.GREEN}/target <host>{C.RESET}    Set target
    {C.GREEN}/tools{C.RESET}            List available tools
    {C.GREEN}/notes{C.RESET}            Show saved findings
    {C.GREEN}/report{C.RESET}           Generate pentest report
    {C.GREEN}/playbook <name>{C.RESET}  Run attack playbook
    {C.GREEN}/playbooks{C.RESET}        List available playbooks
    {C.GREEN}/mcp list{C.RESET}         List MCP servers
    {C.GREEN}/mcp add <n> <cmd>{C.RESET} Add MCP server
    {C.GREEN}/learn{C.RESET}            Learning mode tips
    {C.GREEN}/clear{C.RESET}            Clear chat history
    {C.GREEN}/quit{C.RESET}             Exit
"""


def format_output(text: str) -> str:
    """Apply light formatting to agent output."""
    lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#"):
            lines.append(f"    {C.CYAN}{C.BOLD}{stripped.lstrip('#').strip()}{C.RESET}")
        elif stripped.startswith(("•", "-", "*", "►")) and len(stripped) > 2:
            content = stripped[1:].strip()
            lines.append(f"      {C.GREEN}►{C.RESET} {content}")
        elif stripped and stripped[0].isdigit() and len(stripped) > 1 and stripped[1] in ".)":
            lines.append(f"      {C.YELLOW}{stripped}{C.RESET}")
        elif stripped.startswith("`") or stripped.startswith("$"):
            lines.append(f"      {C.MAGENTA}{stripped}{C.RESET}")
        elif stripped.startswith("[tool]"):
            lines.append(f"      {C.BLUE}{stripped}{C.RESET}")
        elif stripped.startswith("[step"):
            lines.append(f"      {C.DIM}{stripped}{C.RESET}")
        elif stripped:
            lines.append(f"    {stripped}")
        else:
            lines.append("")
    return "\n".join(lines)


def handle_command(cmd: str, args: str, assist: AssistAgent, config: Config) -> str | None:
    """Handle slash commands. Returns response text or None."""

    if cmd == "help" or cmd == "h" or cmd == "?":
        return HELP_TEXT

    elif cmd == "target":
        if not args:
            t = assist.target or "(not set)"
            return f"  Current target: {C.YELLOW}{t}{C.RESET}"
        assist.set_target(args)
        config.target = args
        return f"  Target set: {C.GREEN}{args}{C.RESET}"

    elif cmd == "tools":
        names = get_tool_names()
        tool_list = ", ".join(f"{C.GREEN}{n}{C.RESET}" for n in names)
        return f"  Available tools: {tool_list}"

    elif cmd == "notes":
        notes = _load_notes()
        if not notes:
            return f"  {C.DIM}No notes saved yet.{C.RESET}"
        lines = [f"  {C.YELLOW}{C.BOLD}Saved Findings ({len(notes)}):{C.RESET}"]
        for n in notes[-15:]:
            cat = n.get("category", "?")
            tgt = n.get("target", "")
            content = n["content"][:80]
            lines.append(f"    {C.CYAN}[{cat}]{C.RESET} {C.DIM}{tgt}{C.RESET} {content}")
        return "\n".join(lines)

    elif cmd == "report":
        path = save_report(target=assist.target)
        return f"  Report saved: {C.GREEN}{path}{C.RESET}"

    elif cmd == "playbooks":
        pbs = list_playbooks()
        lines = [f"  {C.YELLOW}{C.BOLD}Available Playbooks:{C.RESET}"]
        for pb in pbs:
            lines.append(f"    {C.GREEN}{pb['name']}{C.RESET} — {pb['description']}")
        return "\n".join(lines)

    elif cmd == "playbook":
        if not args:
            return f"  Usage: /playbook <name>  (use /playbooks to list)"
        if not assist.target:
            return f"  {C.RED}Set a target first: /target <host>{C.RESET}"
        task = build_playbook_task(args, assist.target)
        if not task:
            return f"  {C.RED}Unknown playbook: {args}{C.RESET}"
        # Run as autonomous agent
        auto = AutoAgent(config)
        auto.target = assist.target
        print(f"\n  {C.YELLOW}Running playbook: {args}{C.RESET}")
        print(f"  {C.DIM}Press Ctrl+C to stop{C.RESET}\n")

        def on_step(msg):
            print(f"  {C.DIM}{msg}{C.RESET}")

        try:
            result = auto.run(task, on_step=on_step)
        except KeyboardInterrupt:
            auto.stop()
            result = "[Playbook stopped by user]"
        return f"\n{format_output(result)}"

    elif cmd == "agent":
        if not args:
            return f"  Usage: /agent <task description>"
        auto = AutoAgent(config)
        auto.target = assist.target
        print(f"\n  {C.YELLOW}Agent mode: {args}{C.RESET}")
        print(f"  {C.DIM}Press Ctrl+C to stop{C.RESET}\n")

        def on_step(msg):
            print(f"  {C.DIM}{msg}{C.RESET}")

        try:
            result = auto.run(args, on_step=on_step)
        except KeyboardInterrupt:
            auto.stop()
            result = "[Agent stopped by user]"
        return f"\n{format_output(result)}"

    elif cmd == "mcp":
        parts = args.split(maxsplit=2) if args else []
        if not parts or parts[0] == "list":
            servers = list_mcp_servers()
            if not servers:
                return f"  {C.DIM}No MCP servers configured. Add one with /mcp add <name> <command>{C.RESET}"
            lines = [f"  {C.YELLOW}{C.BOLD}MCP Servers:{C.RESET}"]
            for s in servers:
                lines.append(f"    {C.GREEN}{s['name']}{C.RESET} — {s['command']} {' '.join(s.get('args', []))}")
            return "\n".join(lines)
        elif parts[0] == "add" and len(parts) >= 3:
            name = parts[1]
            command = parts[2]
            result = add_mcp_server(name, command)
            return f"  MCP server added: {C.GREEN}{name}{C.RESET}"
        else:
            return f"  Usage: /mcp list | /mcp add <name> <command>"

    elif cmd == "learn":
        return f"""
  {C.YELLOW}{C.BOLD}Learning Mode:{C.RESET}
    Try these commands:
    {C.GREEN}quiz me on web attacks{C.RESET}
    {C.GREEN}explain sql injection{C.RESET}
    {C.GREEN}quiz reconnaissance 3{C.RESET}
    {C.GREEN}explain buffer overflow{C.RESET}
    {C.GREEN}what tools are used for network scanning?{C.RESET}
"""

    elif cmd == "clear":
        assist.reset()
        return f"  {C.YELLOW}Chat cleared.{C.RESET}"

    elif cmd in ("quit", "exit", "q"):
        print(f"\n  {C.DIM}Goodbye! 👋{C.RESET}\n")
        sys.exit(0)

    return None


def main():
    """Main TUI entry point."""
    config = Config.from_env()

    if not config.api_key:
        print(f"\n  {C.RED}✗ API key not found{C.RESET}")
        print(f"  Create .env file: {C.YELLOW}ANTHROPIC_API_KEY=your-key{C.RESET}\n")
        sys.exit(1)

    # Parse CLI args
    import argparse
    parser = argparse.ArgumentParser(description="Pentrex — AI Pentest Agent")
    parser.add_argument("-t", "--target", help="Set initial target")
    parser.add_argument("--playbook", help="Run a playbook immediately")
    args, _ = parser.parse_known_args()

    if args.target:
        config.target = args.target

    assist = AssistAgent(config)

    print(BANNER)

    if config.target:
        print(f"  {C.GREEN}Target: {config.target}{C.RESET}\n")

    # If playbook specified via CLI, run it
    if args.playbook:
        if not config.target:
            print(f"  {C.RED}Playbook requires a target. Use -t <host>{C.RESET}")
            sys.exit(1)
        result = handle_command("playbook", args.playbook, assist, config)
        if result:
            print(result)
        return

    # Interactive loop
    while True:
        try:
            query = input(f"  {C.GREEN}{C.BOLD}you ➜{C.RESET}  ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n  {C.DIM}Goodbye! 👋{C.RESET}\n")
            break

        if not query:
            continue

        # Handle commands
        if query.startswith("/"):
            parts = query[1:].split(maxsplit=1)
            cmd = parts[0].lower()
            cmd_args = parts[1] if len(parts) > 1 else ""
            result = handle_command(cmd, cmd_args, assist, config)
            if result:
                print(result)
                print(f"\n  {C.DIM}{'─' * 50}{C.RESET}\n")
            continue

        # Regular chat
        print(f"  {C.DIM}thinking...{C.RESET}", end="\r")

        try:
            response = assist.chat(query)
        except Exception as e:
            response = f"Error: {e}"

        print(f"  {' ' * 20}", end="\r")
        print(f"\n  {C.CYAN}{C.BOLD}pentrex ➜{C.RESET}\n")
        print(format_output(response))
        print(f"\n  {C.DIM}{'─' * 50}{C.RESET}\n")


if __name__ == "__main__":
    main()
