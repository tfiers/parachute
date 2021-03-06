from typing import Tuple

import pytest

from parachute import validate_inputs, ArgumentError, either, vector


@validate_inputs
def my_function(
    a: either("xx", bool),
    b: str = "bb",
    c: vector(length=2) = (4.0, 4),
    d: Tuple[str, bool] = ("yes", True),
    e: float = 22.0,
):
    return a


def test_argcheck():
    my_function("xx")
    my_function(False)
    my_function("xx", "whatevs")
    my_function(True, "whatevs")
    my_function(True, "whatevs", (6, -1.2))
    with pytest.raises(ArgumentError):
        my_function(233)
    with pytest.raises(ArgumentError):
        my_function("xy")
    with pytest.raises(ArgumentError):
        my_function("xx", 35)
    with pytest.raises(ArgumentError):
        my_function("xx", "whatevs", False)
    with pytest.raises(ArgumentError):
        my_function("xx", "whatevs", ("a", 88))


def test_return():
    assert my_function("xx") == "xx"
    assert my_function(True) == True
    assert my_function(True, "bb") == True


def test_kwargs():
    assert True  # for vs code test discovery
    my_function(a="xx")
    my_function(a=False)
    my_function(a="xx", b="whatevs")
    my_function(a=True, b="whatevs")
    my_function(a=True, b="whatevs", c=(6, -1.2))
    with pytest.raises(ArgumentError):
        my_function(a=233)
    with pytest.raises(ArgumentError):
        my_function(a="xy")
    with pytest.raises(ArgumentError):
        my_function(a="xx", b=35)
    with pytest.raises(ArgumentError):
        my_function(a="xx", b="whatevs", c=False)
    with pytest.raises(ArgumentError):
        my_function(a="xx", b="whatevs", c=("a", 88))
    with pytest.raises(ArgumentError):
        my_function("xx", b="whatevs", c=("a", 88))
    with pytest.raises(ArgumentError):
        my_function("xx", True, c=("a", 88))


def test_kwarg_out_of_order():
    my_function("xx", d=("jo", False))


def test_int_for_float():
    # An int should work when type = float
    # (typeguard handles this).
    my_function("xx", e=22)


def test_check_default():
    with pytest.raises(ArgumentError):

        @validate_inputs
        def func(a: float = "jojo"):
            pass
