
from typing import Any

def value_type(value: Any) -> str:
    """Return the type of a given value as a string."""
    if isinstance(value, str):
        return "string"
    if isinstance(value, dict):
        return "dictionary"
    if isinstance(value, int):
        return "number"
    if value is None:
        return "null/None"
    try:
        return type(value).__name__
    except Exception:
        return str(type(value))
