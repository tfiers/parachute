import inspect

from typing import Callable, Any
from functools import wraps
from dataclasses import dataclass

from .util import _repr, matches_type
from .spec import Spec


def validate(value, annotation) -> bool:
    """
    Checks whether a value matches a type hint / annotation.
    """
    if annotation is None:
        valid = True
    elif isinstance(annotation, Spec):
        valid = annotation.validate(value)
    else:
        valid = matches_type(value, annotation)
    return valid


def input_validation(function: Callable) -> Callable:
    """
    Decorator that validates function call arguments (and default argument
    values) against argument annotations / type hints.
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


@dataclass
class ArgumentError(Exception):
    """ Raised when a function is called with an invalid argument. """

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
