from abc import ABC, abstractmethod
from inspect import isclass
from typing import TypeVar, Generic, Any, Optional, Tuple, Type

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


class ValidatedArgumentFactory(type, ABC):
    def __new__(mcs, clsname, parents, namespace):
        cls = type.__new__(mcs, clsname, parents, dict(namespace))

        # Check if the given class is a subclass of Validatable (Validatable is
        # a subclass of typing.Generic, and therefore its own subclasses
        # contain an `__orig_bases__` attribute).
        orig_bases = getattr(cls, "__orig_bases__", None)
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
                    value = subclass.cast(argument)
                    cast_was_succesful = True
                except CastingError as error:
                    # Get a default instantiation of the canonical parameter
                    # type (e.g. `0` for int, `()` for tuple, etc).
                    value = subclass.get_dummy_value(canonical_param_type)
                    cast_was_succesful = False
                    casting_error = error

                output = subclass.get_populated_instance(
                    canonical_param_type, value
                )
                output.raw_argument = argument
                output.cast_was_succesful = cast_was_succesful
                if not cast_was_succesful:
                    output.casting_error = casting_error
                return output

            cls.__new__ = __new_subclass__

        return cls


class ValidatedArgument(
    Generic[CanonicalParamType], metaclass=ValidatedArgumentFactory
):
    def is_valid(self) -> bool:
        """
        Whether the instantiation argument could be succesfully cast to the
        output type AND whether the argument was to spec.
        """
        return self.cast_was_succesful and self.is_to_spec()

    @classmethod
    @abstractmethod
    def cast(cls, argument: Any) -> CanonicalParamType:
        """
        Convert the argument to an instance of the canonical
        parameter type. Raise a CastingError when this cannot be
        safely done.

        This is a default implementation, which may be overriden by
        subclasses.
        """
        raise NotImplementedError

    @abstractmethod
    def is_to_spec(self) -> bool:
        """
        Whether the argument conforms to certain constraints that are not
        based on type alone. What it means to be "to spec" is determined by
        subclasses.
        """
        raise NotImplementedError

    @staticmethod
    def get_dummy_value(
        canonical_param_type: Type[CanonicalParamType]
    ) -> CanonicalParamType:
        """
        Get a default instantiation of the canonical parameter type (e.g. `0`
        for int, `()` for tuple, etc).
        """
        return canonical_param_type.__new__(canonical_param_type)

    @classmethod
    def get_populated_instance(
        cls,
        canonical_param_type: Type[CanonicalParamType],
        value: CanonicalParamType,
    ):
        """
        Get an instantiation of a subclass of the canonical parameter type,
        populated with a given value.

        For overriding methods: this subclass instance should be created as

            return canonical_param_type.__new__(cls, [custom args and kwargs]),

        where the custom (keyword) arguments ensure that the instance is
        populated with the given value. Also make sure that the overriding
        method is annotated as a class method!
        """
        return canonical_param_type.__new__(cls, value)


def either(*options):
    """
    Checks whether the function argument matches one of the given options.
    """

    class Choice(ValidatedArgument[object]):

        options_: Tuple[Any, ...] = options

        @classmethod
        def cast(cls, argument: Any):
            """
            Do not attempt any casting (as we do not know what the output
            type should be -- the options could be of different types).
            """
            return argument

        @classmethod
        def get_populated_instance(cls, canonical_param_type, value):
            obj = object.__new__(cls)
            obj.value = value
            return obj

        def is_to_spec(self) -> bool:
            return any(
                Choice.value_matches_option(self.value, option)
                for option in self.options_
            )

        @staticmethod
        def value_matches_option(value: Any, option: Any) -> bool:
            """ Whether a value is a valid input for an option. """
            if isclass(option) and issubclass(option, ValidatedArgument):
                return option(value).is_valid()
            elif util.is_literal(option):
                return value == option
            else:
                return util.is_of_type(value, option)

    return Choice
