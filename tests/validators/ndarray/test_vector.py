import numpy as np

from parachute import vector


def test_vector_complex():
    Vector = vector(complex)
    assert not Vector("not a numeric vector").is_valid()
    assert Vector([1, 2]).is_valid()
    assert Vector((1, 2)).is_valid()
    assert Vector((True, False)).is_valid()
    assert Vector((9.9, False)).is_valid()
    assert Vector(np.array((9.9, False))).is_valid()
    assert Vector([1, 2]).is_valid()
    assert Vector([1, 2, 88.8, False]).is_valid()
    assert Vector([1, 4 - 0.1j]).is_valid()
    assert Vector([1, 2, 88.8, 4 - 0.1j]).is_valid()
    assert Vector(np.array([1, 2, 88.8, 4 - 0.1j])).is_valid()


def test_vector_float():
    Vector = vector()
    assert not Vector("not a numeric vector").is_valid()
    assert Vector([1, 2]).is_valid()
    assert Vector((1, 2)).is_valid()
    assert Vector((True, False)).is_valid()
    assert Vector((9.9, False)).is_valid()
    assert Vector(np.array((9.9, False))).is_valid()
    assert Vector([1, 2]).is_valid()
    assert Vector([1, 2, 88.8, False]).is_valid()
    assert not Vector([1, 4 - 0.1j]).is_valid()
    assert not Vector([1, 2, 88.8, 4 - 0.1j]).is_valid()
    assert not Vector(np.array([1, 2, 88.8, 4 - 0.1j])).is_valid()


def test_vector_int():
    Vector = vector(int)
    assert not Vector("not a numeric vector").is_valid()
    assert Vector([1, 2]).is_valid()
    assert Vector((1, 2)).is_valid()
    assert Vector((True, False)).is_valid()
    assert not Vector((9.9, False)).is_valid()
    assert not Vector(np.array((9.9, False))).is_valid()
    assert Vector([1, 2]).is_valid()
    assert not Vector([1, 2, 88.8, False]).is_valid()
    assert not Vector([1, 4 - 0.1j]).is_valid()
    assert not Vector([1, 2, 88.8, 4 - 0.1j]).is_valid()
    assert not Vector(np.array([1, 2, 88.8, 4 - 0.1j])).is_valid()


def test_vector_bool():
    Vector = vector(bool)
    assert not Vector("not a numeric vector").is_valid()
    assert not Vector([1, 2]).is_valid()
    assert not Vector((1, 2)).is_valid()
    assert Vector((True, False)).is_valid()
    assert not Vector((9.9, False)).is_valid()
    assert not Vector(np.array((9.9, False))).is_valid()
    assert not Vector([1, 2]).is_valid()
    assert not Vector([1, 2, 88.8, False]).is_valid()
    assert not Vector([1, 4 - 0.1j]).is_valid()
    assert not Vector([1, 2, 88.8, 4 - 0.1j]).is_valid()
    assert not Vector(np.array([1, 2, 88.8, 4 - 0.1j])).is_valid()


def test_vector_shape():
    Vector = vector(float, length=2)
    assert not Vector("not a numeric vector").is_valid()
    assert Vector([1, 2]).is_valid()
    assert Vector((1, 2)).is_valid()
    assert Vector((True, False)).is_valid()
    assert Vector((9.9, False)).is_valid()
    assert Vector(np.array((9.9, False))).is_valid()
    assert Vector([1, 2]).is_valid()
    assert not Vector([1]).is_valid()
    assert not Vector([1, 2, 88.8, False]).is_valid()
    assert not Vector([1, 4 - 0.1j]).is_valid()
    assert not Vector([1, 2, 88.8, 4 - 0.1j]).is_valid()
    assert not Vector(np.array([1, 2, 88.8, 4 - 0.1j])).is_valid()
