import numpy as np
import pytest

# from parachute import Vector

pytestmark = pytest.mark.skip


def test_vector_complex():
    v = Vector(complex)
    assert not v.is_valid("not a numeric vector")
    assert v.is_valid([1, 2])
    assert v.is_valid((1, 2))
    assert v.is_valid((True, False))
    assert v.is_valid((9.9, False))
    assert v.is_valid(np.array((9.9, False)))
    assert v.is_valid([1, 2])
    assert v.is_valid([1, 2, 88.8, False])
    assert v.is_valid([1, 4 - 0.1j])
    assert v.is_valid([1, 2, 88.8, 4 - 0.1j])
    assert v.is_valid(np.array([1, 2, 88.8, 4 - 0.1j]))


def test_vector_float():
    v = Vector()
    assert not v.is_valid("not a numeric vector")
    assert v.is_valid([1, 2])
    assert v.is_valid((1, 2))
    assert v.is_valid((True, False))
    assert v.is_valid((9.9, False))
    assert v.is_valid(np.array((9.9, False)))
    assert v.is_valid([1, 2])
    assert v.is_valid([1, 2, 88.8, False])
    assert not v.is_valid([1, 4 - 0.1j])
    assert not v.is_valid([1, 2, 88.8, 4 - 0.1j])
    assert not v.is_valid(np.array([1, 2, 88.8, 4 - 0.1j]))


def test_vector_int():
    v = Vector(int)
    assert not v.is_valid("not a numeric vector")
    assert v.is_valid([1, 2])
    assert v.is_valid((1, 2))
    assert v.is_valid((True, False))
    assert not v.is_valid((9.9, False))
    assert not v.is_valid(np.array((9.9, False)))
    assert v.is_valid([1, 2])
    assert not v.is_valid([1, 2, 88.8, False])
    assert not v.is_valid([1, 4 - 0.1j])
    assert not v.is_valid([1, 2, 88.8, 4 - 0.1j])
    assert not v.is_valid(np.array([1, 2, 88.8, 4 - 0.1j]))


def test_vector_bool():
    v = Vector(bool)
    assert not v.is_valid("not a numeric vector")
    assert not v.is_valid([1, 2])
    assert not v.is_valid((1, 2))
    assert v.is_valid((True, False))
    assert not v.is_valid((9.9, False))
    assert not v.is_valid(np.array((9.9, False)))
    assert not v.is_valid([1, 2])
    assert not v.is_valid([1, 2, 88.8, False])
    assert not v.is_valid([1, 4 - 0.1j])
    assert not v.is_valid([1, 2, 88.8, 4 - 0.1j])
    assert not v.is_valid(np.array([1, 2, 88.8, 4 - 0.1j]))


def test_vector_shape():
    v = Vector(float, length=2)
    assert not v.is_valid("not a numeric vector")
    assert v.is_valid([1, 2])
    assert v.is_valid((1, 2))
    assert v.is_valid((True, False))
    assert v.is_valid((9.9, False))
    assert v.is_valid(np.array((9.9, False)))
    assert v.is_valid([1, 2])
    assert not v.is_valid([1])
    assert not v.is_valid([1, 2, 88.8, False])
    assert not v.is_valid([1, 4 - 0.1j])
    assert not v.is_valid([1, 2, 88.8, 4 - 0.1j])
    assert not v.is_valid(np.array([1, 2, 88.8, 4 - 0.1j]))
