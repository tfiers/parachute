import pytest

from typing import Union
from parachute import Either


def test_either():
    s = Either("a", "b")
    assert s.validate("a")
    assert s.validate("b")
    assert not s.validate("c")
    assert not s.validate(44)


def test_either_multitype():
    s = Either("a", bool)
    assert s.validate("a")
    assert s.validate(True)
    assert s.validate(False)
    assert not s.validate("b")
    assert not s.validate("c")
    assert not s.validate(44)


def test_either_complextypes():
    s = Either("a", Union[bool, str])
    assert s.validate("a")
    assert s.validate("b")
    assert s.validate("whatevs")
    assert s.validate(True)
    assert not s.validate(44)
