from dataclasses import dataclass
from typing import Any
from ..util import is_literal, matches_type, _repr


@dataclass
class Spec:
    """
    Base class for argument validation specifications
    """

    # Subclasses may set `type_` to something more strict than `Any`. When
    # `spec.conforms(value)` is called, the `value` will be checked against
    # `spec._type`.
    type_: type = Any

    def conforms(self, value: Any) -> bool:
        """ Whether a value conforms to this spec """
        return self.type_conforms(value) and self.value_conforms(value)

    def type_conforms(self, value: Any) -> bool:
        return matches_type(value, self.type_)

    def value_conforms(self, value) -> bool:
        """ To be overridden by subclasses """
        return True


class Either(Spec):
    def __init__(self, *options):
        self.options = options
        if self._homogenous_type():
            self.type_ = type(options[0])
        else:
            # Actually
            self.type_ = Any

    def _homogenous_type(self) -> bool:
        first_type = type(self.options[0])
        return all(type(option) == first_type for option in self.options)

    def value_conforms(self, value: Any) -> bool:
        return any(
            self._option_conforms(value, option) for option in self.options
        )

    def _option_conforms(self, value: Any, option: Any) -> bool:
        if is_literal(option):
            return value == option
        else:
            return matches_type(value, option)

    def __repr__(self) -> str:
        option_text = ", ".join(_repr(option) for option in self.options)
        return f"Either({option_text})"
