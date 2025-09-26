import json


def json_dumps(*args, **kwargs):
    """Customize the standard Python JSON dumper."""
    return json.dumps(*args, **kwargs) + "\n"
