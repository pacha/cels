import click

from .version import cels_version
from .patch import cels_patch
from .list import cels_list
from .describe import cels_describe


@click.group(context_settings={"show_default": True})
def cels():
    pass


cels.add_command(cels_version)  # type: ignore
cels.add_command(cels_patch)  # type: ignore
cels.add_command(cels_list)  # type: ignore
cels.add_command(cels_describe)  # type: ignore
