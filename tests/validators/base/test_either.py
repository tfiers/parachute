from typing import Union

from parachute import either


def test_either():
    E1 = either(4, 5)
    assert E1.options_ == (4, 5)
    E2 = either("a", "b", "c")
    assert E2.options_ == ("a", "b", "c")
    assert E1.options_ == (4, 5)


def test_homogeneous():
    Choice = either("a", "b")
    assert Choice("a").is_valid()
    assert Choice("b").is_valid()
    assert not Choice("c").is_valid()
    assert not Choice(44).is_valid()


def test_either_multitype():
    Choice = either("a", bool)
    assert Choice("a").is_valid()
    assert Choice(True).is_valid()
    assert Choice(False).is_valid()
    assert not Choice("b").is_valid()
    assert not Choice("c").is_valid()
    assert not Choice(44).is_valid()


def test_either_complextypes():
    Choice = either("a", Union[bool, str])
    assert Choice("a").is_valid()
    assert Choice("b").is_valid()
    assert Choice("whatevs").is_valid()
    assert Choice(True).is_valid()
    assert not Choice(44).is_valid()
