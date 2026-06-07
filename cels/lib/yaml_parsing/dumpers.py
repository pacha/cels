import yaml

from .field_types import TaggedScalar
from .field_types import TaggedMapping
from .field_types import TaggedSequence
from cels.lib.safe.mutated_dict import MutatedDict
from cels.lib.safe.mutated_list import MutatedList


class SafePreserveTagDumper(yaml.SafeDumper):
    pass


def represent_tagged_scalar(dumper, data):
    return dumper.represent_scalar(data.tag, str(data))


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

# Note: The C dumper (CSafeDumper) can be ~5-10x faster than the Python SafeDumper,
# but it produces slightly different output formatting (e.g., omitting quotes on
# simple strings in tagged scalars). Since the test suite and some users may rely
# on exact output formatting, we keep the Python dumper by default. The C loader
# is used for input parsing since its output format doesn't matter.
#
# If output format flexibility is acceptable, the C dumper can be enabled by
# uncommenting the code below:
#
# try:
#     _CSafePreserveTagDumper = type("CSafePreserveTagDumper", (yaml.CSafeDumper,), {})
#     _CSafePreserveTagDumper.add_representer(TaggedScalar, represent_tagged_scalar)
#     _CSafePreserveTagDumper.add_representer(TaggedSequence, represent_tagged_sequence)
#     _CSafePreserveTagDumper.add_representer(TaggedMapping, represent_tagged_mapping)
#     _CSafePreserveTagDumper.add_representer(MutatedDict, represent_mutated_dict)
#     _CSafePreserveTagDumper.add_representer(MutatedList, represent_mutated_list)
#     SafePreserveTagDumper = _CSafePreserveTagDumper
# except (ImportError, AttributeError, Exception):
#     pass
