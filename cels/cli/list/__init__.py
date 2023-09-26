import click

from .operations import cels_operations


@click.group(name="list", context_settings={"show_default": True})
def cels_list():
    """Help command to list entities."""
    pass


cels_list.add_command(cels_operations)  # type: ignore
