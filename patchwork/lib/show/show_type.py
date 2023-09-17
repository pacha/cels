from typing import Any


def show_type(value: Any) -> str:
    """Return the type of a given value as a string."""
    if isinstance(value, str) or value is str:
        return "string"
    if isinstance(value, dict) or value is dict:
        return "dictionary"
    if isinstance(value, int) or value is int:
        return "number/integer"
    if isinstance(value, float) or value is float:
        return "number/float"
    if value is list:
        return "list"
    if value is None:
        return "null/None"
    try:
        return type(value).__name__
    except Exception:
        return str(type(value))
