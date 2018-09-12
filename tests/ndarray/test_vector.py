import numpy as np

from parachute import Vector


def test_vector_type():
    v = Vector()
    assert not v.is_valid("not a numeric vector")
    assert v.is_valid([1, 2])
