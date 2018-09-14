import inspect
from dataclasses import dataclass
from functools import wraps
from typing import Callable, Any

from .util import _repr, is_of_type
from .validators.base import ValidatedArgument


def is_valid(value, Annotation) -> bool:
    """
    Checks whether a value matches a type hint / annotation.
    """
    if Annotation is None:
        return True
    elif isinstance(Annotation, ValidatedArgument):
        return Annotation(value).is_valid()
    else:
        return is_of_type(value, Annotation)


def input_validated(function: Callable) -> Callable:
    """
    Decorator that validates function call arguments (and default argument
    values) according to argument annotations / type hints.
    """
    spec = inspect.getfullargspec(function)
    # (According to the Python FAQ, the proper name for "argument name" is
    # "parameter").
    arg_names = spec.args
    default_values = spec.defaults
    # Iterate over parameters in reverse: only the last few parameters have
    # default values.
    for arg_name, value in zip(reversed(arg_names), reversed(default_values)):
        check_arg(function, arg_name, value)

    @wraps(function)
    def checked_function(*args, **kwargs):
        for arg_name, value in zip(arg_names, args):
            check_arg(function, arg_name, value)
        for arg_name, value in kwargs.items():
            check_arg(function, arg_name, value)
        return function(*args, **kwargs)

    return checked_function


def check_arg(function: Callable, arg_name: str, value: Any) -> None:
    """
    Displays a helpful error message when a function argument does not match its
    corresponding type hint / annotation.
    """
    Annotation = function.__annotations__.get(arg_name)
    if not is_valid(value, Annotation):
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
