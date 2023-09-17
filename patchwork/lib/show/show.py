from textwrap import shorten


def show(value, width=50, placeholder="..."):
    """Return a safe string that represents the given object."""
    if isinstance(value, str):
        return shorten(f'"{value}"', width=width, placeholder=placeholder)
    if isinstance(value, dict):
        keys = ", ".join(value.keys())
        if keys:
            shortened_keys = shorten(keys, width=width, placeholder=placeholder)
            return f"dictionary with keys [{shortened_keys}]"
        else:
            return "an empty dictionary"
    if isinstance(value, list):
        list_length = len(value)
        if list_length == 0:
            return "an empty list"
        elif list_length == 1:
            shortened_element = shorten(
                str(value[0]), width=width, placeholder=placeholder
            )
            return f"list with one element [{shortened_element}]"
        else:
            str_elements = [str(element) for element in value]
            shortened_elements = shorten(
                ", ".join(str_elements), width=width, placeholder=placeholder
            )
            return f"list with {list_length} elements [{shortened_elements}]"
    return f'"{shorten(str(value), width=width, placeholder=placeholder)}"'
