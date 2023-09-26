from cels.models import Operation
from cels.models import AnnotatedKey
from cels.models import AnnotationConfig


def test_annotated_key_only_key():
    annotation_config = AnnotationConfig()
    annotated_key = AnnotatedKey("field", annotation_config)
    assert annotated_key.key == "field"
    assert annotated_key.annotation is None


def test_annotated_key_only_operation():
    annotation_config = AnnotationConfig()
    annotated_key = AnnotatedKey("field {set}", annotation_config)
    assert annotated_key.key == "field"
    assert annotated_key.annotation.operation == Operation.get("set")
    assert annotated_key.annotation.indices == []


def test_annotated_key_full():
    annotation_config = AnnotationConfig()
    annotated_key = AnnotatedKey("field {insert@1}", annotation_config)
    assert annotated_key.key == "field"
    assert annotated_key.annotation.operation == Operation.get("insert")
    assert annotated_key.annotation.indices == [1]
