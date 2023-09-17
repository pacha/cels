from typing import Any
from typing import Union
from dataclasses import dataclass

from .annotation import Annotation
from .annotation_config import AnnotationConfig


@dataclass
class AnnotatedKey:
    """A dictionary key with an annotation of the kind {operation@index1,index2,...}."""

    key: Any
    annotation: Union[Annotation, None]

    def __init__(self, raw_key, annotation_config: AnnotationConfig):
        # check if the key is not a string
        if not isinstance(raw_key, str):
            self.key = raw_key
            self.annotation = None
            return

        # check if the key is not annotated
        annotation_data = annotation_config.regex.match(raw_key)
        if not annotation_data:
            self.key = raw_key
            self.annotation = None
            return

        # set attributes
        self.key = annotation_data.group(1)
        if annotation_data.group(2):
            self.annotation = Annotation(
                annotation_data.group(2), index_marker=annotation_config.index_marker
            )
        else:
            # if the annotation is empty (eg. "foo {}")
            self.annotation = None
