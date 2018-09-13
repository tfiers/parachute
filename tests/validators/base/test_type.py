from typing import Any

import pytest

# from parachute import TypeValidator

pytestmark = pytest.mark.skip


def test_any():
    v = TypeValidator(Any)
    assert v.is_valid(False)
    assert v.is_valid(4)
    assert v.is_valid(5.3)
    assert v.is_valid(0 + 3j)
    assert v.is_valid("y")
    assert v.is_valid([4, 5.3])
    assert v.is_valid([5.3])


def test_bool():
    v = TypeValidator(bool)
    assert v.is_valid(False)
    assert not v.is_valid(4)
    assert not v.is_valid(5.3)
    assert not v.is_valid(0 + 3j)
    assert not v.is_valid("y")
    assert not v.is_valid([4, 5.3])
    assert not v.is_valid([5.3])


def test_int():
    v = TypeValidator(int)
    assert v.is_valid(False)
    assert v.is_valid(4)
    assert not v.is_valid(5.3)
    assert not v.is_valid(0 + 3j)
    assert not v.is_valid("y")
    assert not v.is_valid([4, 5.3])
    assert not v.is_valid([5.3])


def test_float():
    v = TypeValidator(float)
    assert v.is_valid(False)
    assert v.is_valid(4)
    assert v.is_valid(5.3)
    assert not v.is_valid(0 + 3j)
    assert not v.is_valid("y")
    assert not v.is_valid([4, 5.3])
    assert not v.is_valid([5.3])


def test_complex():
    v = TypeValidator(complex)
    assert v.is_valid(False)
    assert v.is_valid(4)
    assert v.is_valid(5.3)
    assert v.is_valid(0 + 3j)
    assert not v.is_valid("y")
    assert not v.is_valid([4, 5.3])
    assert not v.is_valid([5.3])


def test_str():
    v = TypeValidator(str)
    assert not v.is_valid(False)
    assert not v.is_valid(4)
    assert not v.is_valid(5.3)
    assert not v.is_valid(0 + 3j)
    assert v.is_valid("y")
    assert not v.is_valid([4, 5.3])
    assert not v.is_valid([5.3])


def test_list():
    v = TypeValidator(list)
    assert not v.is_valid(False)
    assert not v.is_valid(4)
    assert not v.is_valid(5.3)
    assert not v.is_valid(0 + 3j)
    assert not v.is_valid("y")
    assert v.is_valid([4, 5.3])
    assert v.is_valid([5.3])
    assert not v.is_valid((6, 7))


def test_tuple():
    v = TypeValidator(tuple)
    assert not v.is_valid(False)
    assert not v.is_valid(4)
    assert not v.is_valid(5.3)
    assert not v.is_valid(0 + 3j)
    assert not v.is_valid("y")
    assert not v.is_valid([4, 5.3])
    assert not v.is_valid([5.3])
    assert v.is_valid((6, 7))


def test_typing_sequence():
    from typing import Sequence

    v = TypeValidator(Sequence[float])
    assert not v.is_valid(False)
    assert not v.is_valid(4)
    assert not v.is_valid(5.3)
    assert not v.is_valid(0 + 3j)
    assert not v.is_valid("y")
    assert v.is_valid([4, 5.3])
    assert v.is_valid([5.3])
    assert v.is_valid((6, 7))
