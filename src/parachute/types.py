import numpy as np

from dataclasses import dataclass
from typing import Tuple, Optional, Any, Union
from .util import check_type, _repr


class Either:
    """
    A 'type' to annotate choice parameters with. For an example, see the
    docstring of argcheck().
    """

    def __init__(self, *options):
        self.options = options

    def __repr__(self):
        option_text = ", ".join(_repr(option) for option in self.options)
        text = f"Either({option_text})"
        return text


DimensionSize = int
Shape = Tuple[DimensionSize, ...]

DimensionSizeSpec = Union[Any, DimensionSize]
ShapeSpec = Optional[Tuple[DimensionSizeSpec, ...]]

DTypeSpec = Union[complex, float, int]


@dataclass
class TensorCheck:

    shape_spec: ShapeSpec
    dtype_spec: DTypeSpec

    def validate(self, value: Any) -> bool:
        try:
            # Normalise tuples, lists, lists of tuples, etc. to ndarrays.
            other = np.array(value, dtype=self.dtype_spec)
        except ValueError:
            valid = False
        else:
            valid_dtype = self._valid_dtype(other.dtype)
            valid_shape = self._valid_shape(other.shape)
            valid = valid_dtype and valid_shape
        return valid

    def _valid_dtype(self, dtype: np.dtype) -> bool:
        if self.dtype_spec is None:
            valid = True
        else:
            valid = np.dtype(self.dtype_spec) == dtype
        return valid

    def _valid_shape(self, shape: Shape) -> bool:
        if self.shape_spec is None:
            valid = True
        elif len(self.shape_spec) != len(shape):
            valid = False
        else:
            valid = all(
                self._valid_dimsize(dimsize_spec, dimsize)
                for (dimsize_spec, dimsize) in zip(self.shape_spec, shape)
            )
        return valid

    def _valid_dimsize(
        self, dimsize_spec: DimensionSizeSpec, dimsize: DimensionSize
    ) -> bool:
        if dimsize_spec is None:
            valid = True
        else:
            valid = dimsize == dimsize_spec
        return valid


def tensor(shape: ShapeSpec = None, dtype: DTypeSpec = float) -> np.ndarray:
    tensor_check = TensorCheck(shape, dtype)
    return tensor_check


def scalar(dtype: DTypeSpec = float):
    return tensor(shape=(), dtype=dtype)


def vector(length: DimensionSizeSpec = Any, dtype: DTypeSpec = float):
    return tensor(shape=(length,), dtype=dtype)


def matrix(
    rows: DimensionSizeSpec = Any,
    cols: DimensionSizeSpec = Any,
    dtype: DTypeSpec = float,
):
    return tensor(shape=(rows, cols), dtype=dtype)
