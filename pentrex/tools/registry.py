"""Tool registration and execution system."""

_REGISTRY = {}


def register(name: str, description: str, parameters: dict, required: list = None):
    """Decorator to register a tool for the agent."""
    if required is None:
        required = list(parameters.keys())

    def decorator(fn):
        _REGISTRY[name] = {
            "fn": fn,
            "schema": {
                "name": name,
                "description": description,
                "input_schema": {
                    "type": "object",
                    "properties": parameters,
                    "required": required,
                },
            },
        }
        return fn
    return decorator


def get_all_tools() -> list:
    """Return tool schemas for the LLM."""
    return [t["schema"] for t in _REGISTRY.values()]


def get_tool_names() -> list:
    """Return registered tool names."""
    return list(_REGISTRY.keys())


def run_tool(name: str, args: dict) -> dict:
    """Execute a registered tool."""
    if name not in _REGISTRY:
        return {"error": f"Unknown tool: {name}"}
    try:
        return _REGISTRY[name]["fn"](**args)
    except Exception as e:
        return {"error": f"{name} failed: {str(e)}"}


def get_tool_info(name: str) -> dict | None:
    """Get schema for a specific tool."""
    if name in _REGISTRY:
        return _REGISTRY[name]["schema"]
    return None
