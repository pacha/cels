import click
from rich import box
from rich.table import Table
from rich.console import Console

from cels.models import Operation


@click.command(name="operations")
def cels_operations():
    """List available patch operations."""

    table = Table(show_header=False, box=box.MINIMAL, safe_box=True)

    table.add_column("Operation", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description")

    for operation in Operation.get_all():
        table.add_row(operation.name, operation.description)

    console = Console()
    console.print(table)
