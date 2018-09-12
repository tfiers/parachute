import numpy as np

from parachute import Vector


def test_vector_type():
    v = Vector(dtype_spec=float)
    assert not v.is_valid("not a numeric vector")
    assert v.is_valid([1, 2])
    assert v.is_valid((1, 2))
    assert v.is_valid((True, False))
    assert v.is_valid([1, 2, 88.8, False])
    assert not v.is_valid([1, 4 - 0.1j])
    assert not v.is_valid([1, 2, 88.8, 4 - 0.1j])
