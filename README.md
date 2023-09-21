<p align="center">
    <img src="docs/cels-logo-header.png" alt="logo" width="100%">
</p>

cels
====

![Tests](https://github.com/pacha/cels/actions/workflows/tests.yaml/badge.svg)
![Type checks](https://github.com/pacha/cels/actions/workflows/type-checks.yaml/badge.svg)
![Code formatting](https://github.com/pacha/cels/actions/workflows/code-formatting.yaml/badge.svg)

_Small command line tool to patch your YAML and JSON files_

## Example

```yaml
# input.yaml
foo:
  bar: 1
  baz: 2
list:
- a
- b
level: 11
```

```yaml
# patch.yaml
foo:
  bar: 100
list {insert}: c
level {delete}: null
```

```
$ cels input.yaml patch.yaml
foo:
  bar: 100
  baz: 2
list:
- a
- b
- c
```

## Features

* It supports patching of YAML, JSON and TOML files.
* Patch files are just snippets of the original file with annotated keys (ie. `{operation}`).
* It supports a wide number of operations (`set`, `delete`, `rename`, `insert`, `extend`, `use`, `link`, `render`).
* It supports patching nested lists by providing indices to the operations (eg. `{delete@0,2}`).
* It can also be used as a Python library to patch Python dictionaries.

## Installation

To install cells, simply use `pip`:
```
pip install cells
```

## Why cels?

TODO

## Usage

TODO

Similar projects/specification documents
----------------------------------------

* [RFC 6902](https://datatracker.ietf.org/doc/html/rfc6902): Proposed standard
  for JSON patch files. The patch files consists on list of changes. They don't
  mimic the original JSON file structure but offer a wide variety of operations.
* [RFC 7396](https://datatracker.ietf.org/doc/html/rfc7396): Proposed standard
  for JSON path files. Unlike RFC 6902, the patches in this case mimic the
  structure of the original JSON file. There are some limitations though: the
  original document can't make use of explicit `null` values and there are no
  operations to handle values in lists.
* [ytt](https://carvel.dev/ytt/): Very complete command line tool to patch YAML
  files. A bit complex.
* [json-patch](https://github.com/evanphx/json-patch): Go implementation of RFC 6902 and
  RFC 7396.
* [python-json-patch](https://github.com/stefankoegl/python-json-patch): Python
  implementation of RFC 6902.
* [yaml-patcher](https://github.com/Canop/yaml-patcher): Command line tool to
  patch YAML files. It only supports one operation at the moment (overriding
  values in the original YAML).
* [yaml-patch](https://github.com/campos-ddc/yaml-patch): Command line tool to
  patch YAML documents passing a list of changes to apply. The patches are not
  YAML documents themselves but a list of paths and values to override/append. It
  can be used as a Python library.
* [yaml-diff-patch](https://github.com/grantila/yaml-diff-patch): Command line
  and npm package that allows to apply RFC 6902 JSON patches to a YAML document.
* [chbrown/rfc6902](https://github.com/chbrown/rfc6902): TypeScript
  implementation of RFC 6902.

