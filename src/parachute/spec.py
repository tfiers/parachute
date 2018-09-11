import numpy as np

from dataclasses import dataclass
from typing import Tuple, Any, Union
from .util import is_literal, matches_type, _repr


class Spec:
    def __init__(self, output_type: type = Any):
        self.output_type = output_type

    def conforms(self, value: Any) -> bool:
        """ Whether a value conforms to this spec. """
        return self.type_conforms(value) and self.value_conforms(value)

    def type_conforms(self, value: Any) -> bool:
        return matches_type(value, self.output_type)

    def value_conforms(self, value) -> bool:
        # type(value) == self.output_type
        return True


class Either(Spec):
    def __init__(self, *options):
        self.options = options
        typo_0 = type(options[0])
        if all(type(option) == typo_0 for option in options):
            self.output_type = typo_0
        else:
            # Actually a Union
            self.output_type = Any

    def __repr__(self) -> str:
        option_text = ", ".join(_repr(option) for option in self.options)
        text = f"Either({option_text})"
        return text

    def value_conforms(self, value: Any) -> bool:
        # conforms = any(validate(value, option) for option in annotation.options)
        conforms = any(
            self.option_conforms(value, option) for option in self.options
        )
        return conforms

    def option_conforms(self, value: Any, option: Any) -> bool:
        if is_literal(option):
            conforms = value == option
        else:
            conforms = matches_type(value, option)
        return conforms


# These Optionals must become Eithers
DimensionSize = int
Shape = Tuple[DimensionSize, ...]


class DimensionSizeSpec(Spec):
    def __init__(self, dimsize=None):
        self.output_type = DimensionSize
        self.dimsize = dimsize

    def value_conforms(self, value: DimensionSize):
        if self.dimsize is None:
            conforms = True
        else:
            conforms = value == self.dimsize
        return conforms


class ShapeSpec(Spec):
    def __init__(self, shape=None):
        self.output_type = Shape
        self.shape = shape

    def value_conforms(self, value: Shape):
        if self.shape is None:
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
