import numpy as np

from dataclasses import dataclass
from typing import Tuple, Any, Union, Sequence
from numbers import Number

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
                DimSize(dimsize_spec).validate(dimsize)
                for (dimsize_spec, dimsize) in zip(self.shape_spec, value)
            )


Scalar = Number
Vector = Sequence[Scalar]
Matrix = Sequence[Vector]
# further: rank 3, 4, 5, ... tensors

TensorType = Union[np.ndarray, Scalar, Vector, Matrix]


class Tensor(Validator):
    def __init__(self, shape_spec: ShapeSpec = Arbitrary):
        self.shape_spec = shape_spec
        self._type = TensorType

    def is_to_spec(self, value):
        return True
