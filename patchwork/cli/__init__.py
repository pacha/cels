import click

from .version import version


@click.group(context_settings={"show_default": True})
def patchwork():
    pass


patchwork.add_command(version)  # type: ignore
