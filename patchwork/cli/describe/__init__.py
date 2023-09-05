import click

from .operation import describe_operation


@click.group(name="describe", context_settings={"show_default": True})
def patchwork_describe():
    """Help command to list entities."""
    pass


patchwork_describe.add_command(describe_operation)  # type: ignore
