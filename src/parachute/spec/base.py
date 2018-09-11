from dataclasses import dataclass
from typing import Any
from abc import ABC, abstractmethod

from ..util import is_literal, is_of_type, _repr, Type


@dataclass
class Validator(ABC):
    """
    Base class for argument validators.
    """

    # Type to check value against.
    # Subclasses may set this to something more strict than `Any`.
    _type: Type = Any

    def validate(self, value: Any) -> bool:
        """ Whether a value conforms to this validator's type and spec """
        return self.is_of_valid_type(value) and self.is_to_spec(value)

    def is_of_valid_type(self, value: Any) -> bool:
        return is_of_type(value, self._type)

    @abstractmethod
    def is_to_spec(self, value: Type) -> bool:
        pass


class TypeValidator(Validator):
    """
    A dummy validator that only checks the type of the argument.
    """

    def __init__(self, _type: Type):
        self._type = _type

    def is_to_spec(self, value):
        return True


class Either(Validator):
    """
    Any choice out of a list of options is valid.
    """

    def __init__(self, *options):
        self.options = options
        if self._homogenous_type():
            self._type = type(self.options[0])
        else:
            # Actually a Union
            self._type = Any

    def _homogenous_type(self) -> bool:
        """ Whether all options are of the same type. """
        first_type = type(self.options[0])
        return all(type(option) == first_type for option in self.options)

    def is_to_spec(self, value: Any) -> bool:
        return any(
            Either._valid_for_option(value, option) for option in self.options
        )

    @staticmethod
    def _valid_for_option(value: Any, option: Any) -> bool:
        if is_literal(option):
            return value == option
        else:
            return is_of_type(value, option)

    def __repr__(self) -> str:
        option_text = ", ".join(_repr(option) for option in self.options)
        return f"Either({option_text})"
