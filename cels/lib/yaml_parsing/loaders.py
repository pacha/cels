import yaml

from .field_types import TaggedScalar
from .field_types import TaggedMapping
from .field_types import TaggedSequence


def preserve_tag(loader, tag_suffix, node):
    tag = f"!{tag_suffix}"
    if isinstance(node, yaml.ScalarNode):
        return TaggedScalar(loader.construct_scalar(node), tag)
    elif isinstance(node, yaml.SequenceNode):
        return TaggedSequence(loader.construct_sequence(node), tag)
    elif isinstance(node, yaml.MappingNode):
        return TaggedMapping(loader.construct_mapping(node), tag)


class SafePreserveTagLoader(yaml.SafeLoader):
    pass


SafePreserveTagLoader.add_multi_constructor("!", preserve_tag)
