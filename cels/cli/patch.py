import sys
from pathlib import Path

import click

from cels.logs import log
from cels.logs import configure_logging
from cels import default
from cels.services import patch_document
from cels.exceptions import CelsError


file_formats = ["yaml", "json", "toml"]
format_extensions = {
    ".yaml": "yaml",
    ".YAML": "yaml",
    ".yml": "yaml",
    ".YML": "yaml",
    ".json": "json",
    ".JSON": "json",
    ".toml": "toml",
    ".TOML": "toml",
}


@click.command(name="patch")
@click.option(
    "-i",
    "--input-format",
    type=click.Choice(file_formats, case_sensitive=False),
    help="Format of the input file. [default: inferred from the input file extension].",
)
@click.option(
    "-p",
    "--patch-format",
    type=click.Choice(file_formats, case_sensitive=False),
    help="Format of the patch file. [default: inferred from the patch file extension].",
)
@click.option(
    "-o",
    "--output-format",
    type=click.Choice(file_formats, case_sensitive=False),
    help="Format of the output file. [default: same format as input].",
)
@click.option(
    "-O",
    "--output-file",
    default="-",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    help="File to write the result to. If not provided, STDOUT is used.",
)
@click.option(
    "--separator",
    default=default.separator,
    help="Character/text to separate patch keys from patch annotations.",
)
@click.option(
    "--left-marker",
    default=default.left_marker,
    help="Character/text to mark the start of a patch annotation.",
)
@click.option(
    "--index-marker",
    default=default.index_marker,
    help="Character/text to mark the start of an index (key/position) in a patch annotation.",
)
@click.option(
    "--right-marker",
    default=default.right_marker,
    help="Character/text to mark the end of a patch annotation.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Show debug information.",
)
@click.argument(
    "input_file",
    type=click.Path(
        exists=True, dir_okay=False, readable=True, allow_dash=True, path_type=Path
    ),
)
@click.argument(
    "patch_file",
    type=click.Path(
        exists=True, dir_okay=False, readable=True, allow_dash=False, path_type=Path
    ),
)
def cels_patch(
    input_file,
    patch_file,
    output_file,
    input_format,
    patch_format,
    output_format,
    separator,
    left_marker,
    index_marker,
    right_marker,
    verbose,
):
    """Patch a yaml, json or toml file."""

    # setup logging
    configure_logging("DEBUG" if verbose else "WARN")

    # infer and normalize input format
    if not input_format:
        try:
            input_format = format_extensions[input_file.suffix]
        except KeyError:
            log.error(
                f"Invalid input format. It must be one of: {', '.join(file_formats)}.",
            )
            sys.exit(1)
    input_format = input_format.lower()

    # infer and normalize patch format
    if not patch_format:
        try:
            patch_format = format_extensions[patch_file.suffix]
        except KeyError:
            log.error(
                f"Invalid patch format. It must be one of: {', '.join(file_formats)}.",
            )
            sys.exit(2)
    patch_format = patch_format.lower()

    # infer and normalize output format
    if not output_format:
        output_format = input_format
    output_format = output_format.lower()

    # compose output
    input_text = input_file.read_text(encoding="utf-8")
    patch_text = patch_file.read_text(encoding="utf-8")
    try:
        output_text = patch_document(
            input_format=input_format,
            input_text=input_text,
            patch_format=patch_format,
            patch_text=patch_text,
            output_format=output_format,
            separator=separator,
            left_marker=left_marker,
            index_marker=index_marker,
            right_marker=right_marker,
        )
    except CelsError as err:
        log.error(f"{err}")
        sys.exit(3)

    # save result
    try:
        with click.open_file(output_file, "w", encoding="utf-8") as f:
            f.write(output_text)
    except OSError as err:
        log.error(f"Error found when saving output file: {err}")
        sys.exit(4)
