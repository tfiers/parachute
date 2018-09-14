import numpy as np

from parachute import shape


def test_shapespec_any():
    Shape = shape(None)
    assert not Shape("not a shapespec").is_valid()
    assert not Shape((4, "4")).is_valid()
    assert not Shape((4, None)).is_valid()
    assert not Shape((None,)).is_valid()
    assert Shape(()).is_valid()
    assert Shape((4,)).is_valid()
    assert Shape((5, 4)).is_valid()
    assert Shape((5, 0)).is_valid()
    assert Shape((5, False)).is_valid()
    assert Shape((5, 42098507180)).is_valid()
    assert Shape((5, 4, 0, 9)).is_valid()


def test_shapespec_fix():
    Shape = shape((5, 4))
    assert not Shape("not a shapespec").is_valid()
    assert not Shape((4, "4")).is_valid()
    assert not Shape((4, None)).is_valid()
    assert not Shape((None,)).is_valid()
    assert not Shape(()).is_valid()
    assert not Shape((4,)).is_valid()
    assert Shape((5, 4)).is_valid()
    assert not Shape((5, 0)).is_valid()
    assert not Shape((5, False)).is_valid()
    assert not Shape((5, 42098507180)).is_valid()
    assert not Shape((5, 4, 0, 9)).is_valid()


def test_shapespec_wildcard():
    Shape = shape((5, None))
    assert not Shape("not a shapespec").is_valid()
    assert not Shape((4, "4")).is_valid()
    assert not Shape((4, None)).is_valid()
    assert not Shape((None,)).is_valid()
    assert not Shape(()).is_valid()
    assert not Shape((4,)).is_valid()
    assert Shape((5, 4)).is_valid()
    assert Shape((5, 0)).is_valid()
    assert Shape((5, False)).is_valid()
    assert Shape((5, 42098507180)).is_valid()
    assert not Shape((5, 4, 0, 9)).is_valid()


def test_non_tuple_iterable():
    Shape = shape()
    assert not Shape(["one", "love"]).is_valid()
    assert Shape([1, 3]).is_valid()
    assert Shape(np.array([1, 3])).is_valid()
    assert Shape((i for i in range(3))).is_valid()
