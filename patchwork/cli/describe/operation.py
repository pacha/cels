
import sys
# import logging as log
import logging

import click
from rich import box
from rich.table import Table
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel

from patchwork.models import Operation
from patchwork.logs import init_logging
from rich.logging import RichHandler

@click.command(name="operation")
@click.argument("operation_name")
def describe_operation(operation_name):
    """Describe an operation."""

    # init_logging("error")

    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(show_time=False)]
    )

    log = logging.getLogger("rich")

    try:
        operation = Operation.get(operation_name)
    except KeyError:
        log.error("Invalid operation.")
        sys.exit(1)

    console = Console()
    console.print(operation.name)
    console.print()
    console.print(operation.description)
    console.print()
    console.print(operation.notes)
    panels = []
    for example in operation.examples:
        console.print(Panel(
            example["code"],
            title=example["title"],
            title_align='left',
            box=box.SQUARE,
            expand=False
        ))
    # console.print(Columns(panels, title="Examples", expand=True, equal=True))
        

