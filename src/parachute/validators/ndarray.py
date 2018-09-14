from typing import Union, Tuple, Type, Optional, Any

import numpy as np

import parachute.util as util
from .base import Validatable, CastingError, either

# Special type to denote arbitrary shapes, dimension sizes, etc.
Arbitrary = None

DType = Union[Type[bool], Type[int], Type[float], Type[complex]]
ShapeType = Tuple[int, ...]
DimSizeSpec = Union[int, Arbitrary]
ShapeSpec = Union[Tuple[DimSizeSpec, ...], Arbitrary]


def dimsize(spec: DimSizeSpec = Arbitrary):
    class DimSize(int, Validatable):
        dimsize_spec = spec

        def __new__(cls, argument: Any):
            try:
                instance = int.__new__(cls, argument)
            except (TypeError, ValueError):
                instance = int.__new__(cls)
                instance._argument_was_castable = False
            return instance

        def is_to_spec(self):
            if self.dimsize_spec is Arbitrary:
                return True
            else:
                return self == self.dimsize_spec

    return DimSize


def shape(spec: ShapeSpec = Arbitrary):
    class Shape(tuple, Validatable):
        shape_spec = spec

        @classmethod
        def cast(cls, argument: Any) -> ShapeType:
            """
            Accepts any iterable, and attempts to cast to a tuple of
            Python int's.
            """
            try:
                if isinstance(argument, np.ndarray):
                    # Convert numpy 'int32'-like types to plain 'int'.
                    argument = argument.tolist()

                tup = tuple(el for el in iter(argument))

                if not util.is_of_type(tup, ShapeType):
                    raise TypeError

            except Exception as err:
                raise CastingError(err)

            else:
                return tuple.__new__(cls, tup)

        def __new__(cls, argument: Any):
            try:
                instance = Shape.cast(argument)
            except CastingError:
                instance = tuple.__new__(cls)
                instance._argument_was_castable = False
            return instance

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

    return Shape


def array(
    #
    # Checks whether the argument is a scalar, a numeric vector, a numeric
    # matrix, or in general, a numeric tensor, of the right shape and data type.
    #
    dtype: DType = float,
    #     Datatype of the numbers in the array.
    ndim: either(int, Arbitrary) = Arbitrary,
    #     Number of dimensions of the array.
    shape: Optional[ShapeSpec] = None,
    #     Shape of the array (e.g. `(10,10,2)` or `(2, Arbitrary)`). If given,
    #     `ndim` is ignored.
):
    if shape is None:
        shape = ndim * (Arbitrary,)

    # Subclass np.ndarray to enable code completion in IDE's.
    # Syntax to correctly do this thanks to:
    # https://sourceforge.net/p/numpy/mailman/message/12594316/
    class Array(np.ndarray, Validatable):
        dtype_spec = dtype
        shape_spec = shape

        def __new__(cls, argument):
            try:
                if not isinstance(argument, np.ndarray):
                    argument = np.array(argument)
                cast = argument.astype(self.dtype_spec, casting="safe")
                instance = np.ndarray.__new__(
                    cls, shape=cast.shape, buffer=cast
                )
            except (TypeError, ValueError):
                instance = np.ndarray.__new__(cls)
                instance._argument_was_castable = False
            return instance

        def is_to_spec(self):
            return True

    return Array
