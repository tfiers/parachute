from typing import Any
from parachute import TypeValidator


def test_any():
    v = TypeValidator(Any)
    assert v.validate(4)
    assert v.validate(5.3)
    assert v.validate(False)
    assert v.validate("y")
    assert v.validate(0 + 3j)
    assert v.validate([4, 5.3])
    assert v.validate([5.3])


def test_float():
    v = TypeValidator(float)
    assert v.validate(4)
    assert v.validate(5.3)
    assert v.validate(False)
    assert not v.validate("y")
    assert not v.validate(0 + 3j)
    assert not v.validate([4, 5.3])
    assert not v.validate([5.3])
