import math
from typing import Union, Tuple, List

Number = Union[int, float]
Vector = Union[Tuple[Number, ...], List[Number]]


# ---------- Validation ----------

def _validate_vector(v: Vector):
    """Validate that the input is a tuple or list of numbers."""
    if not isinstance(v, (list, tuple)):
        raise TypeError("Vector must be a list or tuple.")
    if not all(isinstance(x, (int, float)) for x in v):
        raise TypeError("Vector elements must be int or float.")


def _validate_vectors(a: Vector, b: Vector):
    """Validate that two vectors have the same dimension and numeric elements."""
    _validate_vector(a)
    _validate_vector(b)
    if len(a) != len(b):
        raise ValueError("Vectors must have the same dimension.")


# ---------- Vector Operations ----------

def dot(a: Vector, b: Vector) -> Number:
    """Compute the dot product of two vectors."""
    _validate_vectors(a, b)
    return sum(x * y for x, y in zip(a, b))


def add(a: Vector, b: Vector) -> Tuple[Number, ...]:
    """Add two vectors element-wise."""
    _validate_vectors(a, b)
    return tuple(x + y for x, y in zip(a, b))


def sub(a: Vector, b: Vector) -> Tuple[Number, ...]:
    """Subtract vector b from vector a element-wise."""
    _validate_vectors(a, b)
    return tuple(x - y for x, y in zip(a, b))


def mul_scalar(v: Vector, s: Number) -> Tuple[Number, ...]:
    """Multiply a vector by a scalar."""
    _validate_vector(v)
    if not isinstance(s, (int, float)):
        raise TypeError("Scalar must be int or float.")
    return tuple(x * s for x in v)


def length(v: Vector) -> float:
    """Return the Euclidean length (magnitude) of the vector."""
    _validate_vector(v)
    return math.sqrt(dot(v, v))


def normalize(v: Vector) -> Tuple[float, ...]:
    """Return a unit vector in the same direction as v."""
    _validate_vector(v)
    l = length(v)
    if l == 0:
        return tuple(v)  # Return original zero vector
    return tuple(x / l for x in v)


def opposite(v: Vector) -> Tuple[Number, ...]:
    """Return the vector pointing in the opposite direction."""
    _validate_vector(v)
    return tuple(-x for x in v)