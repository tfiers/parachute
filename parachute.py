import inspect
import typeguard

from typing import Callable, Any
from functools import wraps


class Either:
    """
    A 'type' to annotate choice parameters with. For an example, see the
    docstring of argcheck().
    """

    def __init__(self, *options):
        self.options = options

    def __repr__(self):
        option_text = ", ".join(_repr(option) for option in self.options)
        text = f"Either({option_text})"
        return text


def argcheck(function: Callable) -> Callable:
    """
    Decorator that validates function calls (and default argument values)
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
    # "argument name" AKA "parameter"
    arg_names = spec.args
    default_values = spec.defaults
    for arg_name, value in zip(reversed(arg_names), reversed(default_values)):
        check_arg(function, arg_name, value)

    @wraps(function)
    def checked_function(*args, **kwargs):
        for arg_name, value in zip(arg_names, args):
            check_arg(function, arg_name, value)
        function(*args, **kwargs)

    return checked_function


def check_arg(function: Callable, arg_name: str, value: Any):
    """
    Displays a helpful error message when a function argument does not match its
    corresponding type hint / annotation.
    """
    annotation = function.__annotations__.get(arg_name)
    valid = validate(value, annotation)
    if not valid:
        msg = (
            f"\nArgument '{arg_name}' of function '{function.__name__}'\n"
            f"should match {_repr(annotation)}, but got {_repr(value)} instead."
        )
        raise ValueError(msg)


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


def _repr(x: Any) -> str:
    """
    Formats a literal or a type annotation for pretty printing.
    """
    if type(x) == type:
        text = x.__name__
    elif type(x) == str:
        text = f'"{x}"'
    else:
        text = repr(x)
    return text


def make_docstring(function: Callable):
    """
    Sets the docstring of a function based on its source code.

    I have a peculiar style of documenting function arguments (see e.g.
    plot/signal.py), relying on interleaved comments and Python's type system.
    This function extracts these comments and adds them to the docstring.
    """
    source = inspect.getsource(function)
    source_lines = [l.strip() for l in source.splitlines()]
    # Get first line starting with "def"
    signature_start = next(
        i for (i, line) in enumerate(source_lines) if line[:3] == "def"
    )
    def_line = source_lines[signature_start]
    # If we don't have a multiline function signature, leave the function
    # docstring as is.
    if def_line[-1] != "(":
        return
    # Get first non-comment line ending with ":"
    signature_end = next(
        i
        for (i, line) in enumerate(source_lines)
        if (line[:1] != "#") and (line[-1:] == ":")
    )
    # Signature lines
    lines = source_lines[signature_start + 1 : signature_end]
    num_lines = len(lines)
    comment_lines = [i for i in range(num_lines) if lines[i][0] == "#"]
    arg_lines = [i for i in range(num_lines) if i not in comment_lines]
    header_lines = [i for i in range(num_lines) if i < arg_lines[0]]
    for i in comment_lines:
        lines[i] = lines[i].strip("#")
        lines[i] = "  " + lines[i]
    for i in arg_lines:
        lines[i] = lines[i].strip(",")
    for i in header_lines:
        lines[i] = lines[i].strip()
    new_doc = "\n".join(lines)
    existing_doc = function.__doc__
    if existing_doc is not None:
        new_doc = _trim_lines(existing_doc) + "\n" + new_doc
    function.__doc__ = new_doc


def _trim_lines(string: str):
    lines = [line.strip() for line in string.splitlines()]
    return "\n".join(lines)
