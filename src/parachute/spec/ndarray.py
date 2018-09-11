import numpy as np

from dataclasses import dataclass
from typing import Tuple, Any, Union

from .base import Validator, Either


Arbitrary = None

DimSizeType = int
DimSizeSpec = Union[DimSizeType, Arbitrary]

ShapeType = Tuple[DimSizeType, ...]
ShapeSpec = Union[Tuple[DimSizeSpec, ...], Arbitrary]


@dataclass
class DimSize(Validator):

    _spec: DimSizeSpec = Arbitrary
    _type = DimSizeType

    def _check_spec(self, value: DimSizeType):
        return value == self._spec


@dataclass
class Shape(Validator):
    _spec: ShapeSpec = Arbitrary
    _type = ShapeType

    def _check_spec(self, value: ShapeType):
        if self._spec is Arbitrary:
            conforms = True
        elif len(value) != len(self._spec):
            conforms = False
        else:
            conforms = all(
                DimSize(dimsize_spec).validate(dimsize)
                for (dimsize_spec, dimsize) in zip(self._spec, value)
            )
        return conforms


@dataclass
class Tensor(Validator):
    _spec = Arbitrary

    def _check_spec(self, value):
        return True
