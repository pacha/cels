import click

from patchwork import __version__


@click.command(name="version")
def patchwork_version():
    """Display Patchwork version."""
    print(f"Patchwork version {__version__}")
