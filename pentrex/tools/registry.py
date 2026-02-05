"""Tool registration system."""

_REGISTRY = {}


def register(name: str, description: str, parameters: dict, required: list = None):
    """Decorator to register a tool."""
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


def get_all_tools():
    return [t["schema"] for t in _REGISTRY.values()]


def run_tool(name: str, args: dict):
    if name not in _REGISTRY:
        return {"error": f"Unknown tool: {name}"}
    try:
        return _REGISTRY[name]["fn"](**args)
    except Exception as e:
        return {"error": str(e)}
