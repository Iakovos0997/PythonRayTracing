import math
from typing import Union, Tuple, List

Number = Union[int, float]

class Vector:
    def __init__(self, x, y, z):
        if not all(isinstance(coord, (int, float)) for coord in (x, y, z)):
            raise TypeError("Coordinates must be numeric.")
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

        # Vector addition
    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Operand must be a Vector.")
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    # Vector subtraction
    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Operand must be a Vector.")
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    # Scalar multiplication
    def __mul__(self, scalar):
        if not isinstance(scalar, (int, float)):
            raise TypeError("Operand must be numeric.")
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    __rmul__ = __mul__  # allow scalar * vector

    # Negation
    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)
    
    # Cross product
    def cross(self, other: "Vector") -> "Vector":
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    # Dot product
    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Operand must be a Vector.")
        return self.x * other.x + self.y * other.y + self.z * other.z

    # Length
    def length(self):
        return math.sqrt(self.dot(self))

    # Normalize
    def normalize(self):
        l = self.length()
        if l == 0:
            return Vector(0, 0, 0)
        return Vector(self.x / l, self.y / l, self.z / l)
