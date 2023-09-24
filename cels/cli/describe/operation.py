import sys


import click
from rich import box
from rich.table import Table
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.syntax import Syntax

from cels.logs import log
from cels.models import Operation


@click.command(name="operation")
@click.argument("operation_name")
def describe_operation(operation_name):
    """Describe an operation."""

    try:
        operation = Operation.get(operation_name)
    except KeyError:
        log.error("Invalid operation.")
        sys.exit(1)

    console = Console()
    console.print(operation.format, style="magenta italic", markup=False)
    console.print()
    console.print(operation.description)
    console.print()
    console.print(operation.notes)
    for example in operation.examples:
        console.print()
        console.print("» " + example["title"], style="bold cyan")
        console.print(Syntax(example["code"], "yaml", background_color="default"))
