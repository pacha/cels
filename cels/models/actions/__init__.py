from cels.logs import log
from cels.exceptions import CelsInputError

# define action decorator
# (ensures that all exceptions show the path where they happened)
action_name_prefix_length = len("action_")


def action(action_func):
    def wrapped_func(
        container, key, indices, change_value, patch, path, root_input_dict
    ):
        new_path = (path + key).append(indices)
        action_name = action_func.__name__[action_name_prefix_length:]
        log.info(f"{new_path} [cyan]{{{action_name}}}[/]", extra={"markup": True})
        try:
            return action_func(
                container, key, indices, change_value, patch, path, root_input_dict
            )
        except CelsInputError as err:
            raise CelsInputError(f"{new_path} {{{action_name}}}: {err}")

    return wrapped_func


from .action_keep import action_keep
from .action_set import action_set
from .action_use import action_use
from .action_render import action_render
from .action_link import action_link
from .action_patch import action_patch
from .action_insert import action_insert
from .action_extend import action_extend
from .action_rename import action_rename
from .action_delete import action_delete
from .action_delete_value import action_delete_value

actions = {
    "keep": action_keep,
    "set": action_set,
    "use": action_use,
    "render": action_render,
    "link": action_link,
    "patch": action_patch,
    "insert": action_insert,
    "extend": action_extend,
    "rename": action_rename,
    "delete": action_delete,
    "delete_value": action_delete_value,
}
