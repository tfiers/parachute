from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, Optional, Tuple

import parachute.util as util


class CastingError(Exception):
    """
    Raised when a function argument cannot be cast to the correct
    canonical type for the corresponding function parameter.
    """

    def __init__(self, downstream_error: Optional[Exception] = None):
        self.downstream_error = downstream_error


CanonicalParamType = TypeVar("CanonicalParamType")
# The canonical parameter type is the `main` type of a function argument.
# Consider for example an argument that may be both an np.ndarray, a tuple, and
# a list. When all arguments should be normalised to np.ndarray, then np.ndarray
# is the canonical parameter type.


class Factory(type):
    def __new__(mcs, clsname, parents, namespace):
        cls = type.__new__(mcs, clsname, parents, dict(namespace))

        # Check if the given class is a subclass of Validatable (Validatable is
        # a subclass of typing.Generic, and therefore its own subclasses
        # contain an `__orig_bases__` attribute).
        orig_bases = getattr(cls, "__orig_bases__")
        if orig_bases is not None:
            # Find the type with which Validatable was parametrised (i.e. the
            # `str` in `Validatable[str]`).
            # Note: will this work with subclasses of Validatable-subclasses
            # (e.g. Vector -> Tensor -> Validatable)?
            validatable_type = orig_bases[0]
            canonical_param_type = validatable_type.__args__[0]

            def __new_subclass__(subclass, argument: Any):
                """
                Try to cast an argument of arbitrary type to the canonical
                parameter type, and return the result of this type conversion.

                The class of the returned object is a subclass of both the
                canonical parameter type and of `Validatable`.

                When the argument cannot be cast to the canonical parameter
                type, still returns a default instantiation of this type.
                (This enables code completion in IDE's).
                """
                try:
                    value = subclass.cast(subclass, argument)
                except CastingError:
                    # Get a default instantiation of the canonical parameter
                    # type (e.g. `0` for int, `()` for tuple, etc).
                    value = canonical_param_type.__new__(canonical_param_type)
                    cast_was_succesful = False
                else:
                    cast_was_succesful = True
                output = canonical_param_type.__new__(subclass, value)
                output.raw_argument = argument
                output.cast_was_succesful = cast_was_succesful
                return output

            @staticmethod
            def cast(argument: Any):
                """
                Convert the argument to an instance of the canonical
                parameter type. Raise a CastingError when this cannot be
                safely done.

                This is a default implementation, which may be overriden by
                subclasses.
                """
                try:
                    return canonical_param_type.__new__(
                        canonical_param_type, argument
                    )
                except (TypeError, ValueError) as err:
                    raise CastingError(err)

            cls.__new__ = __new_subclass__
            cls.cast = cast

        return cls


class Validatable(Generic[CanonicalParamType], ABC, metaclass=Factory):

    @abstractmethod
    def is_to_spec(self) -> bool:
        """
        Whether the argument conforms to certain constraints that are not
        based on type alone. What it means to be "to spec" is determined by
        subclasses.
        """
        raise NotImplementedError

    def is_valid(self) -> bool:
        """
        Whether the argument could be succesfully cast to the output
        type AND whether the argument was to spec.
        """
        return self.cast_was_succesful and self.is_to_spec()


def either(*options):
    """
    Checks whether the function argument matches one of the given options.
    """

    class Choice(Validatable[object]):

        options_: Tuple[Any, ...] = options

        @staticmethod
        def cast(argument: Any):
            """
            Do not attempt any casting (as we do not know what the output
            type should be -- the options could be of different types).
            """
            return argument

        def is_to_spec(self) -> bool:
            return any(
                Choice.value_matches_option(self.raw_argument, option)
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
