import inspect

from typing import Callable, Any


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