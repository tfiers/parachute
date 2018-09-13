from typing import Union

import pytest

from parachute import Either

pytestmark = pytest.mark.skip


def test_either():
    s = Either("a", "b")
    assert s.is_valid("a")
    assert s.is_valid("b")
    assert not s.is_valid("c")
    assert not s.is_valid(44)


def test_either_multitype():
    s = Either("a", bool)
    assert s.is_valid("a")
    assert s.is_valid(True)
    assert s.is_valid(False)
    assert not s.is_valid("b")
    assert not s.is_valid("c")
    assert not s.is_valid(44)


def test_either_complextypes():
    s = Either("a", Union[bool, str])
    assert s.is_valid("a")
    assert s.is_valid("b")
    assert s.is_valid("whatevs")
    assert s.is_valid(True)
    assert not s.is_valid(44)
