import logging
from rich.logging import RichHandler


log_format = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=log_format,
    datefmt="",
    handlers=[RichHandler(show_time=False)],
)
log = logging.getLogger("cels")
