import logging

from rich.console import Console
from rich.logging import RichHandler


def configure_logging(level):
    error_console = Console(stderr=True)
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="",
        handlers=[RichHandler(console=error_console, show_time=False, show_path=False)],
    )


log = logging.getLogger("cels")
log.addHandler(logging.NullHandler())
