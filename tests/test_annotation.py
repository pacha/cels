import pytest

from cels.models import Operation
from cels.models import Annotation
from cels.exceptions import CelsInputError


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


def test_annotation_empty_annotation():
    """Annotations can't be empty."""
    with pytest.raises(CelsInputError):
        _ = Annotation("")


def test_annotation_wrong_operation():
    """Test wrong annotation operation."""
    with pytest.raises(CelsInputError):
        _ = Annotation("fly@1")


def test_annotation_wrong_index():
    """Test wrong annotation index."""
    with pytest.raises(CelsInputError):
        _ = Annotation("set@foo")


def test_annotation_wrong_syntax():
    """Test wrong annotation syntax."""
    with pytest.raises(CelsInputError):
        _ = Annotation("set$1")
