import json
from typing import Any
from typing import Dict
from typing import Callable

import yaml

# tomli is included in the Python standard lib from 3.11
try:
    import tomllib as toml
except ModuleNotFoundError:
    import tomli as toml  # type: ignore
import tomli_w

from cels import default
from cels.exceptions import CelsInputError

from .patch_dictionary import patch_dictionary


load_functions: Dict[str, Callable] = {
    "yaml": yaml.safe_load,
    "json": json.loads,
    "toml": toml.loads,
}

dump_functions: Dict[str, Callable] = {
    "yaml": yaml.safe_dump,
    "json": json.dumps,
    "toml": tomli_w.dumps,
}

dump_parameters: Dict[str, Dict[str, Any]] = {
    "yaml": {"sort_keys": False, "allow_unicode": True},
    "json": {"indent": 2, "ensure_ascii": False},
    "toml": {},
}


serialize_exceptions = (yaml.YAMLError, ValueError, TypeError)
deserialize_exceptions = (yaml.YAMLError, toml.TOMLDecodeError, json.JSONDecodeError)


def patch_document(
    input_format: str,
    input_text: str,
    patch_format: str,
    patch_text: str,
    output_format: str,
    separator: str = default.separator,
    left_marker: str = default.left_marker,
    index_marker: str = default.index_marker,
    right_marker: str = default.right_marker,
) -> str:
    """Patch a text-based structured document."""

    # get input dictionary
    try:
        input_dict = load_functions[input_format](input_text) or {}
    except KeyError:
        raise CelsInputError(
            f"Error reading input text: '{input_format}' is not a valid format. "
            f"Valid formats: {', '.join(load_functions.keys())}."
        )
    except deserialize_exceptions as err:
        raise CelsInputError(f"Error while parsing input:\n{err}")

    # get patch dictionary
    try:
        patch_dict = load_functions[patch_format](patch_text) or {}
    except KeyError:
        raise CelsInputError(
            f"Error reading patch: '{patch_format}' is not a valid format. "
            f"Valid formats: {', '.join(load_functions.keys())}."
        )
    except deserialize_exceptions as err:
        raise CelsInputError(f"Error while parsing patch:\n{err}")

    # get output dictionary
    output_dict = patch_dictionary(
        input_dict=input_dict,
        patch_dict=patch_dict,
        separator=separator,
        left_marker=left_marker,
        index_marker=index_marker,
        right_marker=right_marker,
    )

    # serialize output dictionary
    try:
        parameters = dump_parameters[output_format]
        output_text = dump_functions[output_format](output_dict, **parameters)
    except KeyError:
        raise CelsInputError(
            f"Error encoding output: '{output_format}' is not a valid format. "
            f"Valid formats: {', '.join(load_functions.keys())}."
        )
    except serialize_exceptions as err:
        raise CelsInputError(f"Error while encoding output:\n{err}")

    return output_text
