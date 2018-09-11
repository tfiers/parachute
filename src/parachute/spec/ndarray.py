import numpy as np

from dataclasses import dataclass
from typing import Tuple, Any, Union

from .base import Validator, Either


Arbitrary = None

DimSizeType = int
DimSizeSpec = Union[DimSizeType, Arbitrary]

ShapeType = Tuple[DimSizeType, ...]
ShapeSpec = Union[Tuple[DimSizeSpec, ...], Arbitrary]


class DimSize(Validator):
    def __init__(self, _spec: DimSizeSpec = Arbitrary):
        self._spec = _spec
        self._type = DimSizeType

    def _check_spec(self, value: DimSizeType):
        if self._spec is Arbitrary:
            return True
        else:
            return value == self._spec


class Shape(Validator):
    def __init__(self, _spec: ShapeSpec = Arbitrary):
        self._spec = _spec
        self._type = ShapeType

    def _check_spec(self, value: ShapeType):
        if self._spec is Arbitrary:
            return True
        elif len(value) != len(self._spec):
            return False
        else:
            return all(
                DimSize(dimsize_spec).validate(dimsize)
                for (dimsize_spec, dimsize) in zip(self._spec, value)
            )


class Tensor(Validator):
    def __init__(self, _spec=Arbitrary):
        self._spec = _spec
        self._type = Any

    def _check_spec(self, value):
        return True
