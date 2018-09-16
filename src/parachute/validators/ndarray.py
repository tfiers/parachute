from typing import Union, Tuple, Type, Optional, Any

import numpy as np
import parachute.util as util

from .base import ValidatedArgument, CastingError, either

# Special type to denote arbitrary shapes, dimension sizes, etc.
Arbitrary = None

DType = Union[Type[bool], Type[int], Type[float], Type[complex]]
ShapeType = Tuple[int, ...]
DimSizeSpec = Union[int, Arbitrary]
ShapeSpec = Union[Tuple[DimSizeSpec, ...], Arbitrary]


def dimsize(spec: DimSizeSpec = Arbitrary):
    """
    Check whether the argument can be cast to an integer, and whether it
    satisfies the given specification.
    """

    class DimSize(ValidatedArgument[int], int):
        dimsize_spec = spec

        @classmethod
        def cast(cls, argument: Any):
            """
            Convert the argument to an instance of the canonical
            parameter type. Raise a CastingError when this cannot be
            safely done.

            This is a default implementation, which may be overriden by
            subclasses.
            """
            try:
                number = float(argument)
                if number.is_integer():
                    return int(argument)
                else:
                    raise ValueError
            except (TypeError, ValueError) as err:
                raise CastingError(err)

        def is_to_spec(self):
            if self.dimsize_spec is Arbitrary:
                return True
            else:
                return self == self.dimsize_spec

        @classmethod
        def annotation_str(cls) -> str:
            if cls.dimsize_spec is Arbitrary:
                return "*"
            else:
                return str(cls.dimsize_spec)

    return DimSize


def shape(spec: ShapeSpec = Arbitrary):
    """
    Check whether the argument is an array shape, that satisfies the given
    specification.
    """

    class Shape(ValidatedArgument[tuple], tuple):
        shape_spec: ShapeSpec = spec

        @classmethod
        def cast(cls, argument: Any) -> ShapeType:
            """
            Accept any iterable, and attempt to cast it to a tuple of
            Python integers.
            """
            try:
                if isinstance(argument, np.ndarray):
                    # Normalise numpy 'int32'-like to plain 'int'.
                    argument = argument.tolist()
                # Check if the input is iterable
                tup = tuple(el for el in iter(argument))
                # Check if the elements are integers.
                if not util.is_of_type(tup, ShapeType):
                    raise TypeError
            except (TypeError, ValueError) as err:
                raise CastingError(err)
            else:
                return tup

        def is_to_spec(self):
            if self.shape_spec is Arbitrary:
                return True
            elif len(self) != len(self.shape_spec):
                return False
            else:
                return all(
                    dimsize(dimsize_spec)(dimsize_).is_valid()
                    for (dimsize_spec, dimsize_) in zip(self.shape_spec, self)
                )

        @classmethod
        def annotation_str(cls) -> str:
            tup = tuple(
                dimsize(dimsize_spec).annotation_str()
                for dimsize_spec in cls.shape_spec
            )
            return str(tup).replace("'", "")

    return Shape


def array(
    dtype: DType = float,
    #     Datatype of the numbers in the array.
    ndim: either(int, Arbitrary) = Arbitrary,
    #     Number of dimensions of the array. Ignored when a value is specified
    #     for `shape_spec`.
    shape_spec: Optional[ShapeSpec] = None,
    #     Shape of the array (e.g. `(10,10,2)` or `(2, Arbitrary)`).
):
    """
    Checks whether the argument is a scalar, a numeric vector, a numeric
    matrix, or in general, a numeric tensor, of the right shape and data type.
    """
    if (shape_spec is None) and (ndim is not Arbitrary):
        shape_spec = ndim * (Arbitrary,)
    elif shape_spec is None:
        shape_spec = Arbitrary

    class Array(ValidatedArgument[np.ndarray], np.ndarray):
        dtype_ = dtype
        shape_spec_ = shape_spec

        @classmethod
        def cast(cls, argument: Any) -> np.ndarray:
            try:
                if not isinstance(argument, np.ndarray):
                    argument = np.array(argument)
                cast = argument.astype(cls.dtype_, casting="safe")
                return cast
            except (TypeError, ValueError) as err:
                raise CastingError(err)

        @classmethod
        def get_dummy_value(cls):
            return np.array([])

        @classmethod
        def get_populated_instance(cls, value: np.ndarray):
            return np.ndarray.__new__(
                cls, shape=value.shape, dtype=value.dtype, buffer=value
            )

        def is_to_spec(self):
            return shape(self.shape_spec_)(self.shape).is_valid()

        @classmethod
        def annotation_str(cls) -> str:
            return (
                f"np.ndarray-like, with dtype "
                f"{util.pretty_str(cls.dtype_)}-compatible "
                f"and shape according to spec self.shape_spec_"
            )

    return Array


def vector(dtype: DType = float, length: DimSizeSpec = Arbitrary):
    """
    Checks whether the argument is a numeric vector of the right data type and
    length.
    """
    return array(dtype, shape_spec=(length,))
