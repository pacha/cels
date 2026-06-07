import re
from typing import Any
from dataclasses import dataclass

from cels import default
from cels.lib.show import show
from cels.exceptions import CelsInputError

# Cache for AnnotationConfig instances keyed by (separator, left_marker, index_marker, right_marker)
# to avoid re-compiling the same regex when the same config is used repeatedly.
_config_cache: dict = {}


@dataclass
class AnnotationConfig:
    separator: str
    left_marker: str
    index_marker: str
    right_marker: str
    regex: re.Pattern

    def __init__(
        self,
        separator: str = default.separator,
        left_marker: str = default.left_marker,
        index_marker: str = default.index_marker,
        right_marker: str = default.right_marker,
    ):
        # Check cache first
        cache_key = (separator, left_marker, index_marker, right_marker)
        cached = _config_cache.get(cache_key)
        if cached is not None:
            self.separator = cached.separator
            self.left_marker = cached.left_marker
            self.index_marker = cached.index_marker
            self.right_marker = cached.right_marker
            self.regex = cached.regex
            return

        # components
        self.separator = re.escape(separator)
        self.left_marker = re.escape(left_marker)
        self.index_marker = re.escape(index_marker)
        self.right_marker = re.escape(right_marker)

        # annotation regex
        pattern = (
            f"^(.+){ self.separator }{ self.left_marker }(.*){ self.right_marker }$"
        )
        self.regex = re.compile(pattern)

        # Store in cache
        _config_cache[cache_key] = self

    def check_no_annotations(self, value: Any) -> None:
        """Check recursively that there are no annotations in the keys of this dictionary or its children."""
        # Fast path: scalar values cannot contain annotations
        if not isinstance(value, (dict, list)):
            return
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                # Only string keys can have annotations; skip non-string keys quickly
                if isinstance(child_key, str) and self.regex.match(child_key):
                    raise CelsInputError(
                        f"Cannot perform operation in annotated key {show(child_key)}: "
                        "annotations are not allowed if a parent/ancestor key performs an explicit "
                        '"set" operation'
                    )
                self.check_no_annotations(child_value)
        elif isinstance(value, list):
            for element in value:
                self.check_no_annotations(element)
