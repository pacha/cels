<p align="center">
    <img src="docs/cels-logo-header.png" alt="logo" width="100%">
</p>

cels
====

![Tests](https://github.com/pacha/cels/actions/workflows/tests.yaml/badge.svg)
![Type checks](https://github.com/pacha/cels/actions/workflows/type-checks.yaml/badge.svg)
![Code formatting](https://github.com/pacha/cels/actions/workflows/code-formatting.yaml/badge.svg)

_Command line tool to patch your YAML and JSON files_

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

## Description

Cels is a command-line tool and Python library that enables you to make multiple
modifications to YAML, JSON, or TOML documents. These modifications are based on
changes specified in a _patch_ file. The patch file is written in the same
format as the original data and mirrors its structure. For instance, if you want
to change the `bar` key value from `hello` to `bye` in this example:
```
foo:
  bar: hello
```
You simply need to create a patch like this:
```
foo:
  bar: bye
```
For more complex modifications, you can annotate the keys of the patch
document with the operation to perform in the format: `{operation[@index1,
index2, …]}`. For example, to insert an element in the middle of a list, you
only need to specify the new location and the value to insert:
```yaml

# input
list:
- a
- c

# patch
list {insert@1}: b
```
Cels supports a variety of operations (`set`, `delete`, `rename`, `insert`,
`extend`, `use`, `link`, `render`), and most of them can optionally take indices
to work with any level of nested lists.

You can also use Cels as a Python library and incorporate it into your
application if you need to override configuration files (similar to
`docker-compose` overrides).

Refer to [Usage](#usage) for a comprehensive description of all available
operations.

See [Similar Projects](#similar-projects) for a comparison between Cels and
other tools and specifications with similar objectives.

> The name 'Cels' originates from the traditional, non-digital animation world,
> where transparent layers with drawings (cels) were layered on top of each
> other to create the final image.

## Installation

To install cells, simply use `pip`:
```
pip install cells
```

## Usage

TODO

## Similar Projects

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

