import yaml

from .field_types import TaggedScalar
from .field_types import TaggedMapping
from .field_types import TaggedSequence


class SafePreserveTagDumper(yaml.SafeDumper):
    pass


def represent_tagged_scalar(dumper, data):
    return dumper.represent_scalar(data.tag, str(data))


def represent_tagged_sequence(dumper, data):
    return dumper.represent_sequence(data.tag, data)


def represent_tagged_mapping(dumper, data):
    return dumper.represent_mapping(data.tag, data)


SafePreserveTagDumper.add_representer(TaggedScalar, represent_tagged_scalar)
SafePreserveTagDumper.add_representer(TaggedSequence, represent_tagged_sequence)
SafePreserveTagDumper.add_representer(TaggedMapping, represent_tagged_mapping)
