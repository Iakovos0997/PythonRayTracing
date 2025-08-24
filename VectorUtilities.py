import math

def _validate_vectors(a, b):
    if not (isinstance(a, (list, tuple)) and isinstance(b, (list, tuple))):
        raise TypeError("Both operands must be lists or tuples.")
    if len(a) != len(b):
        raise ValueError("Vectors must have the same dimension.")
    if not all(isinstance(x, (int, float)) for x in a+b):
        raise TypeError("Vector elements must be int or float.")

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))

def add(a, b):
    return tuple(x + y for x, y in zip(a, b))

def mul_scalar(v, s):
    return tuple(x * s for x in v)

def length(v):
    return math.sqrt(dot(v, v))

def normalize(v):
    l = length(v)
    if l == 0:
        return v
    return tuple(x / l for x in v)