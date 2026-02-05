from pentrex.tools.registry import get_all_tools, run_tool, register

# Import tools to trigger registration
from pentrex.tools import quiz
from pentrex.tools import explain
from pentrex.tools import toolguide
from pentrex.tools import scenario

__all__ = ["get_all_tools", "run_tool", "register"]
