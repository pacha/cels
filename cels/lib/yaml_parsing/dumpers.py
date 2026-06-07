import yaml

from .field_types import TaggedScalar
from .field_types import TaggedMapping
from .field_types import TaggedSequence
from cels.lib.safe.mutated_dict import MutatedDict
from cels.lib.safe.mutated_list import MutatedList


class SafePreserveTagDumper(yaml.SafeDumper):
    pass


def represent_tagged_scalar(dumper, data):
    # Use explicit single-quote style to ensure both the Python and C dumpers
    # produce identical output for tagged scalars (e.g. !secret 'db_username'
    # instead of !secret db_username). This is critical for output format
    # consistency and test compatibility.
    return dumper.represent_scalar(data.tag, str(data), style="'")


def represent_tagged_sequence(dumper, data):
    return dumper.represent_sequence(data.tag, data)


def represent_tagged_mapping(dumper, data):
    return dumper.represent_mapping(data.tag, data)


def represent_mutated_dict(dumper, data):
    return dumper.represent_dict(data)


def represent_mutated_list(dumper, data):
    return dumper.represent_list(data)


SafePreserveTagDumper.add_representer(TaggedScalar, represent_tagged_scalar)
SafePreserveTagDumper.add_representer(TaggedSequence, represent_tagged_sequence)
SafePreserveTagDumper.add_representer(TaggedMapping, represent_tagged_mapping)
SafePreserveTagDumper.add_representer(MutatedDict, represent_mutated_dict)
SafePreserveTagDumper.add_representer(MutatedList, represent_mutated_list)

# Use C-accelerated dumper when available for significantly faster YAML output.
# The C dumper (CSafeDumper) is ~5-10x faster than the pure-Python SafeDumper.
# We create a subclass of CSafeDumper and register the same representers.
# The represent_tagged_scalar function uses explicit style="'" to ensure
# identical output formatting between Python and C dumpers.
try:
    _CSafePreserveTagDumper = type("CSafePreserveTagDumper", (yaml.CSafeDumper,), {})
    _CSafePreserveTagDumper.add_representer(TaggedScalar, represent_tagged_scalar)
    _CSafePreserveTagDumper.add_representer(TaggedSequence, represent_tagged_sequence)
    _CSafePreserveTagDumper.add_representer(TaggedMapping, represent_tagged_mapping)
    _CSafePreserveTagDumper.add_representer(MutatedDict, represent_mutated_dict)
    _CSafePreserveTagDumper.add_representer(MutatedList, represent_mutated_list)

    # Verify the C dumper works correctly and produces matching output
    _test_data = {"test": TaggedScalar("value", "!tag")}
    _py_out = yaml.dump(_test_data, Dumper=SafePreserveTagDumper, allow_unicode=True)
    _c_out = yaml.dump(_test_data, Dumper=_CSafePreserveTagDumper, allow_unicode=True)
    assert _py_out == _c_out, "C dumper output does not match Python dumper output"

    # C dumper is available and produces matching output - use it as the default
    SafePreserveTagDumper = _CSafePreserveTagDumper
except (ImportError, AttributeError, AssertionError, Exception):
    # Fall back to pure-Python dumper if C dumper is not available or output differs
    pass
