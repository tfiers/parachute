from typing import Callable

import pytest


# Idea 1: Type defined in a function, as a closure


# More descriptive name for the factory functions (make them a class too):
# ValidatableLargeNumberFactory
def large_number(minimumsize=0):
    class LargeNumber(float):
        _minimumsize = minimumsize

        def is_valid(self):
            return self > self._minimumsize

    return LargeNumber


def input_validated(function: Callable) -> Callable:
    def input_validated_function(*args, **kwargs):
        value = args[0]
        Validator = function.__annotations__.get("param")
        v = Validator(value)
        if not v.is_valid():
            raise ValueError
        return function(v, **kwargs)

    return input_validated_function


@input_validated
def g(param: large_number(minimumsize=20)):
    return param


def test_closure():
    g(21)
    with pytest.raises(ValueError):
        g(7)
    with pytest.raises(ValueError):
        g(-3)

    # g returns its argument, so we can inspect it
    assert hasattr(g(44), "is_integer")  # float method
    assert hasattr(g(44), "_minimumsize")


#
#
# Idea 2: Type returned by a classmethod
#
# Problem with this: all instances refer to the same object.


class HugeNumber(float):
    @classmethod
    def get(cls, min=0):
        cls._minimumsize = min
        return cls

    def is_valid(self):
        return self > self._minimumsize


def test_classmethod():
    assert not HugeNumber.get(min=21)(20).is_valid()


#
#
# Idea 3 (doesn't work): override __new__


class RidiculousNumber(float):
    def __new__(cls, min=0):
        cls._minimumsize = min
        return cls

    def __init__(self, num):
        print("never gets here")
        super(float).__init__(num)

    def is_valid(self):
        return self > self._minimumsize


@pytest.mark.xfail
def test___new__():
    R = RidiculousNumber(9999)
    print(R(20))  # --> no instance, but class.
    assert not RidiculousNumber(min=9999)(8).is_valid()


#
#
# Idea 4: metaclasses
# ...
