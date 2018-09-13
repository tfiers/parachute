from typing import Union

import pytest

from parachute import either


def test_either():
    O1 = either(4, 5)
    assert O1.options == (4, 5)
    O2 = either("a", "b", "c")
    assert O1.options == (4, 5)
    assert O2.options == ("a", "b", "c")


@pytest.mark.skip
def test_eitherrr():
    s = Either("a", "b")
    assert s.is_valid("a")
    assert s.is_valid("b")
    assert not s.is_valid("c")
    assert not s.is_valid(44)


@pytest.mark.skip
def test_either_multitype():
    s = Either("a", bool)
    assert s.is_valid("a")
    assert s.is_valid(True)
    assert s.is_valid(False)
    assert not s.is_valid("b")
    assert not s.is_valid("c")
    assert not s.is_valid(44)


@pytest.mark.skip
def test_either_complextypes():
    s = Either("a", Union[bool, str])
    assert s.is_valid("a")
    assert s.is_valid("b")
    assert s.is_valid("whatevs")
    assert s.is_valid(True)
    assert not s.is_valid(44)
