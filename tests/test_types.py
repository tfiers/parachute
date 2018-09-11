import pytest
import numpy as np

from parachute import vector, TensorCheck


def test_vector():
    v = vector(2)
    assert v.validate([1, 2])
    assert v.validate([0.1, -3])
    assert v.validate(np.array([.1, 3]))
    assert v.validate([True, False])
    assert not v.validate([1, 2, 3])
    assert not v.validate(True)
    assert not v.validate([1])


@pytest.mark.xfail
def test_complex():
    v = vector(2, dtype=float)
    assert v.validate([1, 2])
    assert not v.validate([1j, 1 - 3.1j])
    assert not v.validate([1j, 5])
