from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, Optional, Tuple

import parachute.util as util

CanonicalArgType = TypeVar("CanonicalArgType")
# The `main` type of a function argument.
# Consider an example where the argument may be both an np.ndarray, a tuple,
# and a list, but it should be normalised to an np.ndarray (by this package).
# The canonical parameter type is then np.ndarray.

CastedArgument = TypeVar("CastedArgument")
# The type of the argument as it is seen by the function body.
# A subclass of both the canonical parameter type and of `Validatable`.


class CastingError(Exception):
    """
    Raised when a function argument cannot be cast to the correct
    canonical type for the corresponding function parameter.
    """

    def __init__(self, downstream_error: Optional[Exception] = None):
        self.downstream_error = downstream_error


class Validatable(Generic[CanonicalArgType], ABC):
    @classmethod
    @abstractmethod
    def cast(cls, argument: Any) -> CastedArgument:
        """
        Convert the argument to an instance of the output class.
        This is a subclass of both the canonical argument type (e.g. float,
        np.ndarray) and of Validatable.

        Raise a CastingError when this cannot be safely done.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_default_instance(cls) -> CastedArgument:
        """
        Return a default value for the canonical argument type.
        (E.g. `0` for int, `()` for tuple, etc).
        """
        raise NotImplementedError

    @abstractmethod
    def is_to_spec(self: CastedArgument) -> bool:
        """
        Whether the argument conforms to certain constraints that are not
        based on type alone. What it means to be "to spec" is determined by
        subclasses.

        When this method is called, `self` is guaranteed to be of type
        `CastedArgument`. (I.e. a subclass of the canonical argument type).
        """
        raise NotImplementedError

    def __new__(cls, argument: Any) -> CastedArgument:
        """
        Try to cast an argument of arbitrary type to (a subclass of) the
        output type, and return the result of this type conversion.

        When the argument cannot be cast to the output type, still returns a
        default instantiation of the output type. (This enables code
        completion in IDE's).
        """
        try:
            output = cls.cast(cls, argument)
        except CastingError:
            # The value of `output` does not matter, but its type still does.
            output = cls.get_default_instance(cls)
            output._input_was_castable = False
        else:
            output._input_was_castable = True
        return output

    def is_valid(self) -> bool:
        """
        Whether the argument could be succesfully cast to the output
        type AND whether the argument was to spec. (What it means to be "to
        spec" is defined by subclass implementations of `is_to_spec()`).
        """
        return self._input_was_castable and self.is_to_spec()


def either(*options):
    """
    Checks whether the function argument matches one of the given options.
    """

    class Choice(Validatable[Any]):

        options_: Tuple[Any, ...] = options

        def cast(cls, argument: Any):
            """
            Do not attempt any casting (as we do not know what the output
            type should be -- the options could be of different types).

            Save the original argument on a new Choice instance.
            """
            output = object.__new__(cls)
            output.value = argument
            return output

        def get_default_instance(cls):
            """ Never called, as `cast` never raises a casting error. """
            pass

        def is_to_spec(self) -> bool:
            return any(
                Choice.value_matches_option(self.value, option)
                for option in self.options_
            )

        @staticmethod
        def value_matches_option(value: Any, option: Any) -> bool:
            """ Whether a value is a valid input for an option. """
            if util.is_literal(option):
                return value == option
            else:
                return util.is_of_type(value, option)

    return Choice
