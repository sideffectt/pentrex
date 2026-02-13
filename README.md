# Pentrex

AI-powered penetration testing agent. Combines learning, reconnaissance, scanning, and exploitation workflows in a single terminal interface.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)

## What it does

- **Assist mode**: Chat with the agent — you control the flow
- **Agent mode**: Autonomous task execution (recon, scanning, exploitation)
- **Learn mode**: Quiz, explain concepts, tool guides, attack scenarios
- **Terminal tool**: Run nmap, nikto, gobuster, sqlmap directly through the agent
- **Notes system**: Findings saved with categories, persist across sessions
- **Playbooks**: Pre-built attack workflows for web recon and network scanning
- **MCP support**: Extend with external tool servers

## Install

```bash
git clone https://github.com/sideffectt/pentrex.git
cd pentrex

# Setup
python -m venv venv
source venv/bin/activate        # Linux/macOS
# .\venv\Scripts\Activate.ps1  # Windows

pip install -e ".[all]"
```

## Configure

```bash
cp .env.example .env
# Edit .env with your API key
```

```env
ANTHROPIC_API_KEY=sk-ant-...
PENTREX_MODEL=claude-haiku-4-5-20251001
```

Any LiteLLM-supported provider works (OpenAI, Ollama, etc).

## Run

```bash
pentrex                         # Launch TUI
pentrex -t 192.168.1.1          # Launch with target
pentrex run --playbook web_recon -t example.com  # Run playbook
```

## Modes

| Mode | Command | Description |
|------|---------|-------------|
| Assist | (default) | Chat with the agent. You control the flow. |
| Agent | `/agent <task>` | Autonomous single-task execution. |
| Crew | `/crew <task>` | Multi-agent mode. Orchestrator + specialized workers. |
| Learn | `/learn` | Quiz, explanations, tool guides. |

## TUI Commands

```
/agent <task>    Autonomous agent on a task
/crew <task>     Multi-agent crew mode
/target <host>   Set target
/tools           List available tools
/notes           Show saved findings
/report          Generate report
/learn           Enter learning mode
/playbook <name> Run attack playbook
/mcp list        List MCP servers
/clear           Clear chat
/quit            Exit
```

## Playbooks

```bash
pentrex run --playbook web_recon -t example.com
pentrex run --playbook network_scan -t 192.168.1.0/24
```

## Tools

**Built-in:** terminal, nmap, notes, web_search

**MCP:** Configure `mcp_servers.json` for external tools:

```json
{
  "mcpServers": {
    "nmap": {
      "command": "npx",
      "args": ["-y", "gc-nmap-mcp"]
    }
  }
}
```

## Project Structure

```
pentrex/
├── pentrex/
│   ├── agents/          # Agent implementations
│   ├── tools/           # Built-in tools (terminal, nmap, notes, quiz)
│   ├── llm/             # LLM provider wrapper
│   ├── mcp/             # MCP client
│   ├── playbooks/       # Attack playbooks
│   ├── knowledge/       # RAG + learning content
│   ├── runtime/         # Execution environment
│   ├── interface/       # TUI
│   └── config/          # Settings
├── loot/                # Findings output
├── scripts/             # Setup scripts
└── tests/
```

## Legal

Only use against systems you have explicit authorization to test. Unauthorized access is illegal.

## License

MIT
