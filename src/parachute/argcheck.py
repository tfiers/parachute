import typeguard
import inspect

from typing import Callable, Any
from functools import wraps
from dataclasses import dataclass

from .util import _repr
from .types import Either


@dataclass
class ArgumentError(Exception):

    function: Callable
    arg_name: str
    value: Any

    def __repr__(self) -> str:
        annotation = self.function.__annotations__.get(self.arg_name)
        return (
            f"{self.arg_name} (of {self.function.__name__})\n"
            f"should match {_repr(annotation)}, but got "
            f"{_repr(self.value)} (of type {_repr(type(self.value))}) instead."
        )


def input_validation(function: Callable) -> Callable:
    """
    Decorator that validates function call arguments (and default arguments)
    against argument annotations.

    Allows both type checking and basic 'option matching'. Example syntax:

        @validated
        def my_function(
            first_argument: Callable,
            other_argument: str = "Default",
            last_argument: Either("auto", bool) = "auto",
        )
    """
    spec = inspect.getfullargspec(function)
    # According to the Python FAQ, the proper name for "argument name" is
    # "parameter".
    arg_names = spec.args
    default_values = spec.defaults
    # Iterate over arguments in reverse: only the last few parameters have
    # default values.
    for arg_name, value in zip(reversed(arg_names), reversed(default_values)):
        check_arg(function, arg_name, value)

    @wraps(function)
    def checked_function(*args, **kwargs):
        all_args = args + tuple(kwargs.values())
        for arg_name, value in zip(arg_names, all_args):
            check_arg(function, arg_name, value)
        return function(*args, **kwargs)

    return checked_function


def check_arg(function: Callable, arg_name: str, value: Any) -> None:
    """
    Displays a helpful error message when a function argument does not match its
    corresponding type hint / annotation.
    """
    annotation = function.__annotations__.get(arg_name)
    valid = validate(value, annotation)
    if not valid:
        raise ArgumentError(function, arg_name, value)


def validate(value: Any, annotation: Any) -> bool:
    """
    Checks whether a value matches a type hint / annotation.
    """
    if annotation is None:
        valid = True
    elif type(annotation) == Either:
        valid = any(validate(value, option) for option in annotation.options)
    elif type(annotation) == str:
        # A "literal" type hint
        valid = value == annotation
    else:
        try:
            typeguard.check_type("", value, annotation)
            valid = True
        except TypeError:
            valid = False
    return valid
