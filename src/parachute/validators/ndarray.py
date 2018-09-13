from typing import Union, Tuple, Type, Optional, Any

import numpy as np

from .base import Validatable, either

Arbitrary = None
DType = Union[Type[bool], Type[int], Type[float], Type[complex]]
DimSizeSpec = Union[int, Arbitrary]
ShapeSpec = Union[Tuple[DimSizeSpec, ...], Arbitrary]


def dimsize(dimsize: DimSizeSpec = Arbitrary):
    class DimSize(int, Validatable):
        # Try Validatable[BaseType]  :D
        spec = dimsize

        def __new__(cls, argument: Any):
            try:
                instance = int.__new__(cls, argument)
            except (TypeError, ValueError):
                instance = int.__new__(cls)
                instance._argument_was_castable = False
            return instance

        def is_to_spec(self):
            if self.spec is Arbitrary:
                return True
            else:
                return self == self.spec

    return DimSize


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

        def __new__(cls, *args, **kwargs) -> np.ndarray:
            obj = np.ndarray.__new__(cls, shape=None)
            return obj

        def is_to_spec(self):
            pass

    return Array
