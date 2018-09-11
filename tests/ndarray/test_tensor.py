import pytest
import numpy as np

from parachute import Tensor


def test_tensorspec_arbitrary():
    t = Tensor()
    assert not t.validate("No good type")
    assert not t.validate(["a", "b"])
    assert t.validate(3.2)
    assert t.validate([1, 2])
    assert t.validate((5, 6))
    assert t.validate([[1, 2], [4, 4]])
    assert t.validate([[True]])
    assert t.validate([(False)])
    # fmt: off
    assert t.validate(np.array([
        [[1], [2]],
        [[3], [4]],
    ]))
    # fmt: on


@pytest.mark.xfail
def test_tensorspec_higher_order():
    t = Tensor()
    assert t.validate(((((4)))))
    # fmt: off
    assert t.validate([
        [[1], [2]],
        [[3], [4]],
    ])
    # fmt: on
