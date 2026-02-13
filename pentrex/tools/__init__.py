"""Pentrex tools package."""

from pentrex.tools.registry import get_all_tools, run_tool, get_tool_names, get_tool_info

# Import tools to trigger registration
from pentrex.tools import terminal
from pentrex.tools import nmap_tool
from pentrex.tools import notes
from pentrex.tools import quiz
from pentrex.tools import explain

__all__ = ["get_all_tools", "run_tool", "get_tool_names", "get_tool_info"]
