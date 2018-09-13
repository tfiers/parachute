from numbers import Number
from typing import Tuple, Union, Sequence, Type

import numpy as np

from .base import Validator, Either

Arbitrary = None

DimSizeType = int
DimSizeSpec = Union[DimSizeType, Arbitrary]


class DimSize(Validator):
    def __init__(self, dimsize_spec: DimSizeSpec = Arbitrary):
        self.dimsize_spec = dimsize_spec
        self._type = DimSizeType

    def is_to_spec(self, value: DimSizeType):
        if self.dimsize_spec is Arbitrary:
            return True
        else:
            return value == self.dimsize_spec


ShapeType = Tuple[DimSizeType, ...]
ShapeSpec = Union[Tuple[DimSizeSpec, ...], Arbitrary]


class Shape(Validator):
    def __init__(self, shape_spec: ShapeSpec = Arbitrary):
        self.shape_spec = shape_spec
        self._type = ShapeType

    def is_to_spec(self, value: ShapeType):
        if self.shape_spec is Arbitrary:
            return True
        elif len(value) != len(self.shape_spec):
            return False
        else:
            return all(
                DimSize(dimsize_spec).is_valid(dimsize)
                for (dimsize_spec, dimsize) in zip(self.shape_spec, value)
            )


PythonScalar = Number
PythonVector = Sequence[PythonScalar]
PythonMatrix = Sequence[PythonVector]
# further: rank 3, 4, 5, ... tensors

TensorType = Union[np.ndarray, PythonScalar, PythonVector, PythonMatrix]


DTypeSpec = Union[Type[bool], Type[int], Type[float], Type[complex]]

# Syntax to correctly subclass np.ndarray thanks to
# https://sourceforge.net/p/numpy/mailman/message/12594316/
class Tensor(Validator, np.ndarray):
    """
    Checks whether the argument is a scalar, a numeric vector, a numeric matrix,
    or in general, a numeric tensor, of the right shape and data type.

    Subclasses np.ndarray to enable code completion in IDE's.
    """

    def __new__(cls, *args, **kwargs) -> np.ndarray:
        obj = np.ndarray.__new__(cls, shape=None)
        return obj

    def __init__(
        self, dtype_spec: DTypeSpec = float, shape_spec: ShapeSpec = Arbitrary
    ):
        # Only for IDE's (because `is_of_valid_type` is overridden):
        self._type = TensorType
        self.dtype_spec = dtype_spec
        self.shape_spec = shape_spec

    def is_of_valid_type(self, value):
        """
        Checks whether a value can be safely cast to an ndarray of the
        correct data type.
        """
        try:
            if not isinstance(value, np.ndarray):
                value = np.array(value)
            value.astype(self.dtype_spec, casting="safe")
            return True
        except (TypeError, ValueError):
            return False

    def is_to_spec(self, value):
        return Shape(self.shape_spec).is_valid(np.shape(value))


class Vector(Tensor):
    """
    Checks whether the argument is a numeric vector of the right data type and
    length.
    """

    def __init__(
        self, dtype_spec: DTypeSpec = float, length: DimSizeSpec = Arbitrary
    ):
        super().__init__(dtype_spec, (length,))


class Array(Tensor):
    """
    Checks whether the argument is a numeric array with the right data type and
    number of dimensions.
    """

    def __init__(
        self,
        dtype_spec: DTypeSpec = float,
        ndim: Either(Arbitrary, int) = Arbitrary,
    ):
        shape_spec = ndim * (Arbitrary,)
        super().__init__(dtype_spec, shape_spec)
