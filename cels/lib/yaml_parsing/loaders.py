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

# Use C-accelerated loader when available for significantly faster YAML parsing.
# The C loader (CSafeLoader) is ~9x faster than the pure-Python SafeLoader.
# We create a subclass of CSafeLoader and register the same tag-preserving
# multi-constructor to maintain full compatibility with tagged YAML values.
try:
    _CSafePreserveTagLoader = type(
        "CSafePreserveTagLoader", (yaml.CSafeLoader,), {}
    )
    _CSafePreserveTagLoader.add_multi_constructor("!", preserve_tag)

    # Verify the C loader works correctly with our multi-constructor
    _test_result = yaml.load("test: !tag value", Loader=_CSafePreserveTagLoader)
    assert isinstance(_test_result, dict) and "test" in _test_result
    assert isinstance(_test_result["test"], TaggedScalar)

    # C loader is available and working - use it as the default
    SafePreserveTagLoader = _CSafePreserveTagLoader
    _USE_C_LOADER = True
except (ImportError, AttributeError, AssertionError, Exception):
    # Fall back to pure-Python loader if C loader is not available or fails
    _USE_C_LOADER = False
