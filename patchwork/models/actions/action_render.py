from jinja2 import Template
from jinja2 import TemplateError

from patchwork.exceptions import PatchworkInputError
from patchwork.lib.safe import safe_set
from patchwork.lib.safe import safe_traverse
from . import action


@action
def action_render(output_dict, key, indices, change_value, input_dict, patch, path):
    """Set the value pointed by a path in input_dict as new value."""

    # get container to modify
    container, index = safe_traverse(output_dict, key, indices)

    # get value
    try:
        template = Template(change_value)
        rendered_value = template.render(**patch.get_all_vars())
    except TemplateError as err:
        raise PatchworkInputError(
            f"Can't render provided template '{change_value}': {err}."
        )

    # perform action
    safe_set(container, index, rendered_value)
