from .show_value import show_value


def show_index(index, container):
    """Return human friendly string that represents 'index'."""
    index_type = "key" if isinstance(container, dict) else "index"
    index_object = show_value(index)
    return f"{index_type} {index_object}"
