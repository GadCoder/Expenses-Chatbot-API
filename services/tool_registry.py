from typing import Callable, Dict

TOOL_REGISTRY: Dict[str, Callable] = {}


def register_tool(func: Callable) -> Callable:
    """
    Decotorator used to register a function in the TOOL_REGISTRY
    """
    TOOL_REGISTRY[func.__name__] = func
    return func
