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


class ValidatedArgument(ABC, Generic[CanonicalParamType]):
    def __new__(cls, argument: Any):
        """
        Return a new ValidatedArgument instance, populated with the given
        argument.

        For subclasses of ValidatedArgument, the returned instance is a
        subclass of both ValidatedArgument AND of the canonical parameter type.

        The argument is cast to the canonical parameter type before
        populating the new instance. When this type conversion cannot be
        performed succesfully, the new instance is populated with a dummy
        value of the canonical parameter type.
        """
        try:
            value = cls.cast(argument)
            cast_was_succesful = True
        except CastingError as error:
            value = cls.get_dummy_value()
            cast_was_succesful = False
            casting_error = error

        instance = cls.get_populated_instance(value)
        # Accessing the raw argument should not be necessary. But we're not
        # gonna be purist here, and let users of the package access it if
        # they want.
        instance.raw_argument = argument
        instance.cast_was_succesful = cast_was_succesful
        if not cast_was_succesful:
            instance.casting_error = casting_error
        return instance

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

    @classmethod
    @abstractmethod
    def annotation_str(cls) -> str:
        """
        A string representation of this class when used as a type hint /
        parameter annotation.
        """
        raise NotImplementedError

    @classmethod
    def get_dummy_value(cls) -> CanonicalParamType:
        """
        Get a default instantiation of the canonical parameter type (e.g. `0`
        for int, `()` for tuple, etc).
        """
        T = cls._get_canonical_param_type()
        return T.__new__(T)

    @classmethod
    def get_populated_instance(cls, value: CanonicalParamType):
        """
        Get an instantiation of a subclass of the canonical parameter type,
        populated with a given value.

        For overriding methods: this subclass instance should be created as

            return canonical_param_type.__new__(cls, [custom args and kwargs]),

        where the custom arguments ensure that the instance is populated with
        the given value. Also make sure that the overriding method is annotated
        as a class method!
        """
        T = cls._get_canonical_param_type()
        return T.__new__(cls, value)

    @classmethod
    def _get_canonical_param_type(cls) -> CanonicalParamType:
        """
        Find the type with which ValidatedArgument was parametrised (i.e. the
        `str` in `ValidatedArgument[str]`)
        """
        # Note: will this work with subclasses of subclasses
        # (e.g. ValidatedArgument -> Tensor -> Vector)?
        validatable_type = cls.__orig_bases__[0]
        canonical_param_type = validatable_type.__args__[0]
        return canonical_param_type


def either(*options):
    """
    Checks whether the function argument matches one of the given options.
    """

    class Choice(ValidatedArgument[Any]):

        options_: Tuple[Any, ...] = options

        @classmethod
        def annotation_str(cls):
            return f"One of {set(options)}"

        @classmethod
        def cast(cls, argument: Any):
            """
            Do not attempt any casting (as we do not know what the output
            type should be -- the options could be of different types).
            """
            return argument

        @classmethod
        def get_populated_instance(cls, value):
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
            if util.is_of_type(option, ValidatedArgument):
                return option(value).is_valid()
            elif util.is_literal(option):
                return value == option
            else:
                return util.is_of_type(value, option)

    return Choice
