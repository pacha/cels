import click

from cels import __version__


@click.command(name="version")
def cels_version():
    """Display Cels version."""
    print(f"Cels {__version__}")
