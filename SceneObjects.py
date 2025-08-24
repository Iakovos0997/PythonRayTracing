import math
from VectorUtilities import add, sub, dot
from typing import List, Tuple, Optional, Union

Number = Union[int, float]
Vector = Tuple[Number, Number, Number]


# ---------- Scene ----------

class Scene:
    """Represents a 3D scene with objects and lights."""
    def __init__(self, objects: List['SceneObject'], lights: List['Light']):
        self.objects = objects
        self.lights = lights


# ---------- Scene Objects ----------

class SceneObject:
    """
    Base class for all objects in the scene.
    Requires a color attribute and an intersect(O, D) method.
    """
    def __init__(self, color: Tuple[int, int, int]):
        self.color = color

    def intersect(self, O: Vector, D: Vector) -> Optional[Tuple[Number, Number]]:
        raise NotImplementedError("Subclasses must implement the intersect method.")


class Sphere(SceneObject):
    """
    Sphere object in 3D space.
    """
    def __init__(
        self,
        center: Vector,
        radius: float = 1.0,
        color: Tuple[int, int, int] = (255, 0, 0),
        specular: int = 500
    ):
        super().__init__(color)
        self.center = center
        self.radius = radius
        self.specular = specular

    def intersect(self, O: Vector, D: Vector) -> Optional[Tuple[Number, Number]]:
        """
        Solve quadratic equation to find intersection of ray O + t*D with the sphere.
        Returns two t-values or None if no intersection.
        """
        CO = sub(O, self.center)
        a = dot(D, D)
        b = 2 * dot(CO, D)
        c = dot(CO, CO) - self.radius**2

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None

        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b + sqrt_disc) / (2 * a)
        t2 = (-b - sqrt_disc) / (2 * a)
        return (t1, t2)


# ---------- Lights ----------

class Light:
    """Base class for lights."""
    def __init__(self, type_: str, intensity: float):
        self.type = type_
        if not (0.0 <= intensity <= 1.0):
            raise ValueError("Light intensity must be between 0 and 1.")
        self.intensity = intensity


class AmbientLight(Light):
    """Ambient light (uniform, directionless)."""
    def __init__(self, intensity: float):
        super().__init__(type_="ambient", intensity=intensity)


class PointLight(Light):
    """Point light located at a specific position in space."""
    def __init__(self, intensity: float, position: Vector):
        super().__init__(type_="point", intensity=intensity)
        if not (isinstance(position, (list, tuple)) and len(position) == 3):
            raise TypeError("Position must be a 3-element tuple or list.")
        self.position = tuple(position)


class DirectionalLight(Light):
    """Directional light with a specified direction vector."""
    def __init__(self, intensity: float, direction: Vector):
        super().__init__(type_="directional", intensity=intensity)
        if not (isinstance(direction, (list, tuple)) and len(direction) == 3):
            raise TypeError("Direction must be a 3-element tuple or list.")
        self.direction = tuple(direction)
