from datetime import datetime
from typing import Union, Any, Type, Tuple, Generic, TypeVar

from parachute import is_literal, is_python_type, is_typing_type


def test_literal():
    assert is_literal("jo")
    assert not is_literal(str)


# fmt: off
class A: pass
class B: pass
class C(A, B): pass
# fmt: on

python_types = (
    str,
    float,
    dict,
    list,
    object,
    type,
    tuple,
    set,
    datetime,
    A,
    B,
    C,
)
python_literals = (
    "jo",
    88,
    {},
    dict(),
    {"a": 99},
    None,
    datetime(2018, 9, 13),
    A(),
    B(),
    C(),
)
typing_types = (
    Type,
    Union[str, int],
    Any,
    Tuple[float, float],
    TypeVar(""),
    Generic[TypeVar("")],
)


def test_pythontypes():
    for val in python_literals:
        assert not is_python_type(val)

    for val in python_types:
        assert is_python_type(val)

    for val in typing_types:
        assert not is_python_type(val)


def test_typing_types():
    for val in python_literals:
        assert not is_typing_type(val)

    for val in python_types:
        assert not is_typing_type(val)

    for val in typing_types:
        assert is_typing_type(val)
