from typing import Tuple
from parachute import input_validation, ArgumentError, Either

import pytest


@input_validation
def my_function(
    a: Either("xx", bool), b: str = "bb", c: Tuple[float, float] = (4.0, 4)
):
    return a


@pytest.mark.skip
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


@pytest.mark.skip
def test_return():
    assert my_function("xx") == "xx"
    assert my_function(True) == True
    assert my_function(True, "bb") == True


@pytest.mark.skip
def test_kwargs():
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
