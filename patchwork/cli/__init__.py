import click

from .version import patchwork_version
from .patch import patchwork_patch
from .list import patchwork_list
from .describe import patchwork_describe


@click.group(context_settings={"show_default": True})
def patchwork():
    pass


patchwork.add_command(patchwork_version)  # type: ignore
patchwork.add_command(patchwork_patch)  # type: ignore
patchwork.add_command(patchwork_list)  # type: ignore
patchwork.add_command(patchwork_describe)  # type: ignore
