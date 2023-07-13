import click

from patchwork import __version__


@click.command()
def version():
    """Display version."""
    print(f"Patchwork version {__version__}")
