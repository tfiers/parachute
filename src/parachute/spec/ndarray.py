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


DTypeSpec = Either(
    int,
    float,
    complex,
    np.dtype(np.uint),
    np.dtype(int),
    np.dtype(float),
    np.dtype(complex),
)


@dataclass
class TensorSpec:

    shape_spec: ShapeSpec
    dtype_spec: DTypeSpec

    def validate(self, value: Any) -> bool:
        try:
            # Normalise tuples, lists, lists of tuples, etc. to ndarrays.
            other = np.array(value, dtype=self.dtype_spec)
        except ValueError:
            conforms = False
        except TypeError:
            conforms = False
        else:
            valid_dtype = self._valid_dtype(other.dtype)
            valid_shape = matches_type(self.shape_spec, other.shape)
            conforms = valid_dtype and valid_shape
        return conforms

    def _valid_dtype(self, dtype: np.dtype) -> bool:
        if self.dtype_spec is None:
            conforms = True
        else:
            conforms = np.dtype(self.dtype_spec) == dtype
        return conforms


def tensor(shape: ShapeSpec = None, dtype: DTypeSpec = float) -> np.ndarray:
    spec = TensorSpec(shape, dtype)
    return spec


def scalar(dtype: DTypeSpec = float):
    return tensor(shape=(), dtype=dtype)


def vector(length: DimensionSizeSpec = Any, dtype: DTypeSpec = float):
    return tensor(shape=(length,), dtype=dtype)


def matrix(
    shape: Tuple[DimensionSizeSpec, DimensionSizeSpec] = (Any, Any),
    dtype: DTypeSpec = float,
):
    return tensor(shape=shape, dtype=dtype)
