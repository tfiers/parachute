import typing
from inspect import isclass, getsource
from typing import Callable, Any, Type

import typeguard
from parachute.validators.base import ValidatedArgument


def is_literal(value: Any) -> bool:
    return not is_type(value)


def is_type(value: Any) -> bool:
    """
    Whether a value is a python `type`, such as `bool` or `str`, a custom
    defined class, or one of the types from the `typing` module.
    """
    return isclass(value) or is_typing_type(value)


def is_typing_type(value: Any) -> bool:
    """
    Whether a value is one of the types from the `typing` module (such as
    `Sequence[int]`, `Union[bool, str]`, or `Any`).
    """
    return type(value) in (
        typing._GenericAlias,
        typing._VariadicGenericAlias,
        typing._SpecialForm,
        typing.TypeVar,
    )


def is_of_type(value: Any, ttype: Type) -> bool:
    """
    Returns whether a value is of a given type.
    """
    if is_type(ttype):
        if ttype == ValidatedArgument:
            return isclass(value) and issubclass(value, ValidatedArgument)
        else:
            # Defer to the "typeguard" package:
            try:
                typeguard.check_type("value", value, expected_type=ttype)
                return True
            except TypeError:
                return False
    else:
        msg = f"Argument `ttype` must be a type, but got {pretty_str(ttype)}."
        raise TypeError(msg)


def make_docstring(function: Callable):
    """
    Sets the docstring of a function based on its source code.

    I have a peculiar style of documenting function arguments (see e.g.
    plot/signal.py), relying on interleaved comments and Python's type system.
    This function extracts these comments and adds them to the docstring.
    """
    source = getsource(function)
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


def pretty_str(x: Any) -> str:
    """
    Formats types for pretty printing.
    """
    if is_of_type(x, ValidatedArgument):
        text = x.get_annotation_str()
    elif type(x) == type:
        # We want `int` instead of `<class 'int'>`
        text = x.__name__
    else:
        text = repr(x)
    return text
