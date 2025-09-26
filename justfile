
project_dir := justfile_directory()

export PYTHONPATH := project_dir

@help:
  just --list

@test-all:
  uv run pytest --capture=no -o log_cli=false tests/

@test *params:
  uv run pytest -x --capture=no -o log_cli=true {{ params }}

@format:
  uv run black {{ project_dir }}

@type-check:
  uv run mypy {{ project_dir }}/cels/

@cli:
  uv run ipython

@setup:
  uv run pip install -e ".[dev]"
