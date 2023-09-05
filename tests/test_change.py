
import pytest

from patchwork.models import Change
from patchwork.models import Operation
from patchwork.exceptions import PatchworkInputError

def test_change_create():
    """Create a change object."""
    change = Change(
        operation=Operation.get("set"),
        value="some string")
    assert change.operation.name == "set"
    assert change.value == "some string"
    assert change.indices == []

def test_change_wrong_value_type():
    """Try to create a change object with a value unsupported by the provided operation."""
    with pytest.raises(PatchworkInputError):
        _ = Change(
            operation=Operation.get("extend"),
            value="some string")

def test_change_wrong_index():
    """Try to create a change object with a index unsupported by the provided operation."""
    with pytest.raises(PatchworkInputError):
        _ = Change(
            operation=Operation.get("rename"),
            value="some string",
            indices=[3]
        )

def test_change_create_from_dict():
    """Create a change object using a dictionary."""
    change = Change.from_dict({
        "operation": "set",
        "value": "some string"
    })
    assert change.operation.name == "set"
    assert change.value == "some string"
    assert change.indices == []

def test_change_missing_value():
    """For some operations the value is not required"""
    _ = Change.from_dict({
        "operation": "delete",
    })

    with pytest.raises(PatchworkInputError):
        _ = Change.from_dict({
            "operation": "set",
        })

