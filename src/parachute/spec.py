import numpy as np

from dataclasses import dataclass
from typing import Tuple, Any, Union
from .util import is_literal, matches_type, _repr


@dataclass
class Spec:
    """
    Base class for argument validation specifications.
    """

    # Subclasses may set `type_` to a more stricter type than `Any`. When
    # `spec.conforms(value)` is called, the value will be checked against this
    # type.
    type_: type = Any

    def conforms(self, value: Any) -> bool:
        """ Whether a value conforms to this spec. """
        return self.type_conforms(value) and self.value_conforms(value)

    def type_conforms(self, value: Any) -> bool:
        return matches_type(value, self.type_)

    def value_conforms(self, value) -> bool:
        return True


class Either(Spec):
    def __init__(self, *options):
        self.options = options
        if self._homogenous_type():
            self.type_ = type(options[0])
        else:
            # Actually a Union
            self.type_ = Any

    def _homogenous_type(self) -> bool:
        first_type = type(self.options[0])
        return all(type(option) == first_type for option in self.options)

    def value_conforms(self, value: Any) -> bool:
        return any(
            self._option_conforms(value, option) for option in self.options
        )

    def _option_conforms(self, value: Any, option: Any) -> bool:
        if is_literal(option):
            return value == option
        else:
            return matches_type(value, option)

    def __repr__(self) -> str:
        option_text = ", ".join(_repr(option) for option in self.options)
        return f"Either({option_text})"


DimensionSize = int
Shape = Tuple[DimensionSize, ...]


class DimensionSizeSpec(Spec):
    def __init__(self, dimsize=None):
        self.type_ = DimensionSize
        self.dimsize = dimsize

    def value_conforms(self, value: DimensionSize):
        if self.dimsize is None:
            conforms = True
        else:
            conforms = value == self.dimsize
        return conforms


class ShapeSpec(Spec):
    def __init__(self, shape=None):
        self.type_ = Shape
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
