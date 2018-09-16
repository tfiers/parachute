import numpy as np

from parachute import array, shape, Arbitrary


def test_type_arbitrary():
    Array = array()
    assert not Array("No good type").is_valid()
    assert not Array(["a", "b"]).is_valid()
    assert Array(3.2).is_valid()
    assert Array([1, 2]).is_valid()
    assert Array((5, 6)).is_valid()
    assert Array([[1, 2], [4, 4]]).is_valid()
    assert Array([[True]]).is_valid()
    assert Array([(False)]).is_valid()
    # fmt: off
    assert Array(np.array([
        [[1], [2]],
        [[3], [4]],
    ])).is_valid()
    # fmt: on


def test_type_arbitrary_higher_order():
    Array = array()
    assert Array(((((4))))).is_valid()
    # fmt: off
    assert Array([
        [[1], [2]],
        [[3], [4]],
    ]).is_valid()
    # fmt: on


# See test_vector.py for tests of other dtypes.


def test_shape():
    Array = array(shape_spec=(2,))
    assert Array([1, 2]).is_valid()
    assert Array((0.41, -4)).is_valid()
    assert Array(np.array([1, 2])).is_valid()
    assert not Array([1]).is_valid()
    assert not Array([1, 2, 3]).is_valid()
    assert not Array([[1, 2]]).is_valid()


def test_ndim_0():
    Array = array(ndim=0)
    assert Array(1).is_valid()
    assert not Array([1, 2]).is_valid()
    assert not Array([[1, 2], [3, 4]]).is_valid()
    assert not Array([[[1, 2], [3, 4]]]).is_valid()


def test_ndim_1():
    Array = array(ndim=1)
    assert not Array(1).is_valid()
    assert Array([1, 2]).is_valid()
    assert not Array([[1, 2], [3, 4]]).is_valid()
    assert not Array([[[1, 2], [3, 4]]]).is_valid()


def test_ndim_2():
    Array = array(ndim=2)
    assert not Array(1).is_valid()
    assert not Array([1, 2]).is_valid()
    assert Array([[1, 2], [3, 4]]).is_valid()
    assert not Array([[[1, 2], [3, 4]]]).is_valid()


def test_repr():
    Array = array(complex, ndim=2)
    shape_str = shape((Arbitrary, Arbitrary)).get_annotation_str()
    expected_str = (
        "NumPy ndarray-like, with numeric type "
        "compatible with `complex`, "
        f"and shape according to {shape_str}"
    )
    assert Array.get_annotation_str() == expected_str
