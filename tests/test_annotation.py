import pytest

from patchwork.models import Operation
from patchwork.models import Annotation
from patchwork.exceptions import PatchworkInputError


def test_annotation_create():
    """Create a basic annotation."""
    annotation = Annotation("insert@2")
    assert annotation.operation == Operation.get("insert")
    assert annotation.indices == [2]


def test_annotation_set():
    """Create set annotation."""
    annotation = Annotation("set")
    assert annotation.operation == Operation.get("set")
    assert annotation.indices == []


def test_annotation_set_with_index():
    """Create set annotation with index."""
    annotation = Annotation("set@1")
    assert annotation.operation == Operation.get("set")
    assert annotation.indices == [1]


def test_annotation_set_with_negative_index():
    """Create set annotation with negative index."""
    annotation = Annotation("set@-2")
    assert annotation.operation == Operation.get("set")
    assert annotation.indices == [-2]


def test_annotation_wrong_operation():
    """Test wrong annotation operation."""
    with pytest.raises(PatchworkInputError):
        _ = Annotation("fly@1")


def test_annotation_wrong_index():
    """Test wrong annotation index."""
    with pytest.raises(PatchworkInputError):
        _ = Annotation("set@foo")


def test_annotation_wrong_syntax():
    """Test wrong annotation syntax."""
    with pytest.raises(PatchworkInputError):
        _ = Annotation("set$1")
