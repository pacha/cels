
import click

from .operations import patchwork_operations


@click.group(name="list", context_settings={"show_default": True})
def patchwork_list():
    """Help command to list entities."""
    pass


patchwork_list.add_command(patchwork_operations)  # type: ignore
