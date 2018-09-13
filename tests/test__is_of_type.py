from typing import Union, Tuple, Any, Type, TypeVar

from parachute import is_of_type


# fmt: off
class A:
    pass

class B:
    pass

class C(A):
    pass

class D(B, C):
    pass

# fmt: on


def test_pythontypes():
    assert is_of_type("yo", str)
    assert not is_of_type("yo", float)
    assert is_of_type(A(), A)
    assert is_of_type(C(), A)
    assert not is_of_type(C(), B)


def test_multiple_inheritance():
    assert is_of_type(D(), A)
    assert is_of_type(D(), B)
    assert is_of_type(D(), C)


def test_Union():
    assert is_of_type("jo", Union[str, float])
    assert is_of_type(88, Union[str, float])
    assert not is_of_type({"I": 44}, Union[str, float])

    assert is_of_type(D(), Union[A, B])
    assert is_of_type(C(), Union[D, B, C])
    assert not is_of_type(C(), Union[D, B])

    assert is_of_type(D(), Any)


def test_Tuple():
    assert is_of_type(("aa", str), Tuple[str, Type[str]])
    assert is_of_type((D(), "aa"), Tuple[D, str])


def test_TypeVar():
    T = TypeVar("T")
    assert is_of_type(T, TypeVar)
    # Can't test is_of_type(..., T) I think
