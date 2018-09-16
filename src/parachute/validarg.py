import inspect
from functools import wraps
from typing import Callable, Any

from parachute.util import is_of_type, pretty_str
from parachute.validators.base import ValidatedArgument


def is_valid(value, Annotation) -> bool:
    """
    Checks whether a value matches a type hint / annotation.
    """
    if Annotation is None:
        return True
    elif is_of_type(Annotation, ValidatedArgument):
        validated_argument = Annotation(value)
        return validated_argument.is_valid()
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


class ArgumentError(Exception):
    """ Raised when a function is called with an invalid argument. """

    def __init__(self, function: Callable, arg_name: str, value: Any):
        self.function = function
        self.arg_name = arg_name
        self.value = value

    def __repr__(self) -> str:
        annotation = self.function.__annotations__.get(self.arg_name)
        header = "Argument did not match parameter annotation."
        info = {
            "Function": self.function.__qualname__,
            "Parameter": self.arg_name,
            "Annotation": pretty_str(annotation),
            "Argument": pretty_str(self.value),
            "Argument type": pretty_str(type(self.value)),
        }
        info_lines = [f"{name: <14} {val}" for name, val in info.items()]
        msg = header + "\n" + "\n".join(info_lines)
        return msg

    # Must override __str__ of Exception to get nice print in tracebacks.
    __str__ = __repr__
