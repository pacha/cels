from .key_location import KeyLocation
from .path import Path
from .annotated_key import AnnotatedKey
from .annotation import Annotation
from .annotation_config import AnnotationConfig
from .operation import Operation
from .change import Change
from .patch import Patch

import yaml
from cels.paths import data_path

# initialize operation
operations_data_path = data_path / "operations.yaml"
operations_list = yaml.safe_load(operations_data_path.read_text())
for opertation_item in operations_list["operations"]:
    Operation.add(**opertation_item)
