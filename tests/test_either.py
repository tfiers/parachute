import pytest

from typing import Union
from parachute import Either


def test_either():
    s = Either("a", "b")
    assert s.conforms("a")
    assert s.conforms("b")
    assert not s.conforms("c")
    assert not s.conforms(44)


def test_either_multitype():
    s = Either("a", bool)
    assert s.conforms("a")
    assert s.conforms(True)
    assert s.conforms(False)
    assert not s.conforms("b")
    assert not s.conforms("c")
    assert not s.conforms(44)


def test_either_complextypes():
    s = Either("a", Union[bool, str])
    assert s.conforms("a")
    assert s.conforms("b")
    assert s.conforms("whatevs")
    assert s.conforms(True)
    assert not s.conforms(44)
