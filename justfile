
project_dir := justfile_directory()

export PYTHONPATH := project_dir

@help:
  just --list

@test-all:
  pytest --capture=no -o log_cli=false tests/

@test *params:
  pytest --capture=no -o log_cli=true {{ params }}

@format:
  black {{ project_dir }}

@check:
  mypy {{ project_dir }}/patchwork/

@cli:
  ipython

run *params:
  #!/usr/bin/env python3
  from patchwork.cli import patchwork
  params = "{{ params }}".split()
  patchwork(params)

