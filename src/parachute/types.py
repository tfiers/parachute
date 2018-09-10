from .util import _repr


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
