from typing import Union

import numpy as np

from parachute import either, vector


def test_different_objects():
    C1 = either(4, 5)
    assert C1.options_ == (4, 5)
    C2 = either("a", "b", "c")
    assert C2.options_ == ("a", "b", "c")
    assert C1.options_ == (4, 5)


def test_homogeneous_type():
    Choice = either("a", "b")
    assert Choice("a").is_valid()
    assert Choice("b").is_valid()
    assert not Choice("c").is_valid()
    assert not Choice(44).is_valid()


def test_multitype():
    Choice = either("a", bool)
    assert Choice("a").is_valid()
    assert Choice(True).is_valid()
    assert Choice(False).is_valid()
    assert not Choice("b").is_valid()
    assert not Choice("c").is_valid()
    assert not Choice(44).is_valid()


def test_complextypes():
    Choice = either("a", Union[bool, str])
    assert Choice("a").is_valid()
    assert Choice("b").is_valid()
    assert Choice("whatevs").is_valid()
    assert Choice(True).is_valid()
    assert not Choice(44).is_valid()


def test_validated_types():
    Choice = either("a", vector(int, length=2))
    assert Choice("a").is_valid()
    assert not Choice("b").is_valid()
    assert Choice([1, 2]).is_valid()
    assert Choice(np.array((4, 4))).is_valid()
    assert not Choice((4.0, 2.0)).is_valid()
    assert not Choice((4.1, 2.0)).is_valid()
    assert not Choice([1, 2, 3]).is_valid()
    assert not Choice([1]).is_valid()
    assert not Choice([[1, 2]]).is_valid()
