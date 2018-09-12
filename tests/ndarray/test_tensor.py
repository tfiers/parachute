import pytest
import numpy as np

from parachute import Tensor


def test_tensortype_arbitrary():
    t = Tensor()
    assert not t.is_valid("No good type")
    assert not t.is_valid(["a", "b"])
    assert t.is_valid(3.2)
    assert t.is_valid([1, 2])
    assert t.is_valid((5, 6))
    assert t.is_valid([[1, 2], [4, 4]])
    assert t.is_valid([[True]])
    assert t.is_valid([(False)])
    # fmt: off
    assert t.is_valid(np.array([
        [[1], [2]],
        [[3], [4]],
    ]))
    # fmt: on


def test_tensortype_higher_order():
    t = Tensor()
    assert t.is_valid(((((4)))))
    # fmt: off
    assert t.is_valid([
        [[1], [2]],
        [[3], [4]],
    ])
    # fmt: on


def test_tensor_shape():
    t = Tensor(shape_spec=(2,))
    assert t.is_valid([1, 2])
    assert t.is_valid((0.41, -4))
    assert t.is_valid(np.array([1, 2]))
    assert not t.is_valid([1, 2, 3])
    assert not t.is_valid([[1, 2]])
