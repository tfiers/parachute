from dataclasses import dataclass
from typing import Any, Tuple, TypeVar
from abc import ABC, abstractmethod

from ..util import is_literal, is_of_type, _repr


Spec = TypeVar("GenericSpec")
Type = TypeVar("GenericType")


@dataclass
class Validator(ABC):
    """
    Base class for type and spec validators.
    """

    # Specification to check value against (see subclasses for examples).
    _spec: Spec

    # Type to check value against.
    # Subclasses may set this to something more strict than `Any`.
    _type: Type = Any

    def validate(self, value: Any) -> bool:
        """ Whether a value conforms to this validator's _type and _spec """
        return self._valid_type(value) and self._check_spec(value)

    def _valid_type(self, value: Any) -> bool:
        return is_of_type(value, self._type)

    @abstractmethod
    def _check_spec(self, value: Type) -> bool:
        pass


class TypeValidator(Validator):
    """
    A dummy validator that only checks the type of the argument.
    """

    def __init__(self, _type: Type):
        self._type = _type
        self._spec = None

    def _check_spec(self, value):
        return True


class Either(Validator):
    """
    Any choice out of a list of options is valid.
    """

    def __init__(self, *options):
        self._spec = options
        if self._homogenous_type():
            self._type = type(self._spec[0])
        else:
            # Actually a Union
            self._type = Any

    def _homogenous_type(self) -> bool:
        """ Whether all options are of the same type. """
        first_type = type(self._spec[0])
        return all(type(option) == first_type for option in self._spec)

    def _check_spec(self, value: Any) -> bool:
        return any(
            self._valid_for_option(value, option) for option in self._spec
        )

    def _valid_for_option(self, value: Any, option: Any) -> bool:
        if is_literal(option):
            return value == option
        else:
            return is_of_type(value, option)

    def __repr__(self) -> str:
        option_text = ", ".join(_repr(option) for option in self._spec)
        return f"Either({option_text})"
