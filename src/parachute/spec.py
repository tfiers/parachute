import numpy as np

from dataclasses import dataclass
from typing import Tuple, Any, Union
from .util import matches_type, _repr


class Spec:
    def __init__(self, typpe: type = Any):
        self.typpe = typpe

    def conforms(self, value: Any) -> bool:
        """ Whether a value conforms to this spec. """
        return self.valid_type(value)

    def valid_type(self, value: Any) -> bool:
        return matches_type(value, self.typpe)


class Either(Spec):
    def __init__(self, *options):
        self.options = options

    def __repr__(self) -> str:
        option_text = ", ".join(_repr(option) for option in self.options)
        text = f"Either({option_text})"
        return text

    def conforms(self, value: Any) -> bool:
        # conforms = any(validate(value, option) for option in annotation.options)
        conforms = True
        return conforms


# These Optionals must become Eithers
DimensionSize = int
Shape = Tuple[DimensionSize, ...]


class DimensionSizeSpec(Spec):
    def __init__(self, dimsize: DimensionSize = None):
        self.typpe = DimensionSize
        self.dimsize = dimsize

    def conforms(self, value):
        if not self.valid_type(value):
            conforms = False
        elif self.dimsize is None:
            conforms = True
        else:
            conforms = value == self.dimsize
        return conforms


class ShapeSpec(Spec):
    def __init__(self, shape: Shape = None):
        self.typpe = Shape
        self.shape = shape

    def conforms(self, value):
        if not self.valid_type(value):
            conforms = False
        elif self.shape is None:
            conforms = True
        elif len(value) != len(self.shape):
            conforms = False
        else:
            conforms = all(
                DimensionSizeSpec(dimsize_spec).conforms(dimsize)
                for (dimsize_spec, dimsize) in zip(self.shape, value)
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
