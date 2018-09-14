from abc import ABC, abstractmethod
from typing import Any, Optional

import parachute.util as util


class CastingError(Exception):
    """
    Raised when a function argument cannot be cast to the correct type for
    the corresponding parameter.
    """

    def __init__(self, downstream_error: Optional[Exception] = None):
        self.downstream_error = downstream_error


class Validatable(ABC):

    _argument_was_castable = True

    def is_valid(self) -> bool:
        """ Whether a value conforms to this validator's type and spec. """
        return self._argument_was_castable and self.is_to_spec()

    @abstractmethod
    def is_to_spec(self) -> bool:
        ...


def either(*options):
    class Choice(Validatable):
        options_ = options

        def __init__(self, value):
            self.value = value

        def is_to_spec(self) -> bool:
            return any(
                self._value_matches_option(self.value, option)
                for option in self.options_
            )

        @staticmethod
        def _value_matches_option(value: Any, option: Any) -> bool:
            if util.is_literal(option):
                return value == option
            else:
                return util.is_of_type(value, option)

    return Choice
