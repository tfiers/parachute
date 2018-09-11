import numpy as np

from dataclasses import dataclass
from typing import Tuple, Any

from ..util import is_literal, matches_type
from .base import Spec, Either


DimensionSize = int
Shape = Tuple[DimensionSize, ...]


class DimensionSizeSpec(Spec):
    def __init__(self, dimsize_spec=None):
        self.type_ = DimensionSize
        self.dimsize_spec = dimsize_spec

    def value_conforms(self, value: DimensionSize):
        if self.dimsize_spec is None:
            conforms = True
        else:
            conforms = value == self.dimsize_spec
        return conforms


class ShapeSpec(Spec):
    def __init__(self, shape_spec=None):
        self.type_ = Shape
        self.shape_spec = shape_spec

    def value_conforms(self, value: Shape):
        if self.shape_spec is None:
            conforms = True
        elif len(value) != len(self.shape_spec):
            conforms = False
        else:
            conforms = all(
                DimensionSizeSpec(dimsize_spec).conforms(dimsize)
                for (dimsize_spec, dimsize) in zip(self.shape_spec, value)
            )
        return conforms


@dataclass
class TensorSpec(Spec):
    tensor_spec = None
