"""MCP (Model Context Protocol) client for external tool integration."""

import json
import os
import subprocess

MCP_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "mcp_servers.json")


def load_mcp_config() -> dict:
    """Load MCP server configuration."""
    path = os.path.abspath(MCP_CONFIG_PATH)
    if not os.path.exists(path):
        return {"mcpServers": {}}
    with open(path, "r") as f:
        return json.load(f)


def list_mcp_servers() -> list:
    """List configured MCP servers."""
    config = load_mcp_config()
    servers = config.get("mcpServers", {})
    return [
        {"name": name, "command": s.get("command", ""), "args": s.get("args", [])}
        for name, s in servers.items()
    ]


def add_mcp_server(name: str, command: str, args: list = None, env: dict = None):
    """Add a new MCP server to config."""
    config = load_mcp_config()
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    server = {"command": command}
    if args:
        server["args"] = args
    if env:
        server["env"] = env

    config["mcpServers"][name] = server

    path = os.path.abspath(MCP_CONFIG_PATH)
    with open(path, "w") as f:
        json.dump(config, f, indent=2)

    return {"added": name, "command": command}


def remove_mcp_server(name: str) -> bool:
    """Remove an MCP server from config."""
    config = load_mcp_config()
    if name in config.get("mcpServers", {}):
        del config["mcpServers"][name]
        path = os.path.abspath(MCP_CONFIG_PATH)
        with open(path, "w") as f:
            json.dump(config, f, indent=2)
        return True
    return False


# Note: Full MCP stdio transport requires async implementation.
# This is the configuration layer. For full MCP protocol support,
# integrate with mcp-python SDK: pip install mcp
