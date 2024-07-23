from jinja2 import Template
from jinja2 import TemplateError

from cels.models import Path
from cels.exceptions import CelsInputError
from cels.lib.safe import safe_set
from cels.lib.safe import safe_traverse
from . import action


@action
def action_render(
    output_dict, key, indices, change_value, patch, path, root_input_dict
):
    """Render a template using variables defined in the patch dictionary."""

    def get(path: str):
        """Get a value from the input dict given a dotted-notation path."""
        input_path = Path(path)
        value = input_path.get_value(root_input_dict)
        return value

    # get container to modify
    container, index = safe_traverse(output_dict, key, indices)

    # get value
    try:
        template = Template(change_value)
        rendered_value = template.render(_get=get, **patch.get_all_vars())
    except TemplateError as err:
        raise CelsInputError(f"Can't render provided template '{change_value}': {err}.")

    # perform action
    safe_set(container, index, rendered_value)
