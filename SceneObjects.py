import math
from VectorUtilities import Vector
from typing import List, Tuple, Optional, Union

Number = Union[int, float]


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
        CO = O - self.center
        a = D.dot(D)
        b = 2 * D.dot(CO)
        c = CO.dot(CO) - self.radius**2

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None

        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b + sqrt_disc) / (2 * a)
        t2 = (-b - sqrt_disc) / (2 * a)
        return (t1, t2)

# class Cylinder(SceneObject):
#     def __init__(
#         self,
#         base_center: Vector,
#         radius: float = 1.0,
#         height: float = 1.0,
#         color: Tuple[int, int, int] = (255, 0, 0),
#         specular: int = 500
#     ):
#         super().__init__(color)
#         self.base_center = base_center
#         self.radius = radius
#         self.height = height
#         self.specular = specular

#     def intersect(self, O, D):
        
#         # Step 1: Compute quadratic coefficients for infinite cylinder along Y-axis
#         a = D[0]**2 + D[2]**2
#         b = 2 * ((O[0] - self.base_center[0]) * D[0] + (O[2] - self.base_center[2]) * D[2])
#         c = (O[0] - self.base_center[0])**2 + (O[2] - self.base_center[2])**2 - self.radius**2

#         discriminant = b**2 - 4 * a * c
#         if discriminant < 0:
#             return None # No intersection
        
#         # Step 2: Solve quadratic for t-values
#         sqrt_disc = math.sqrt(discriminant)
#         t1 = (-b - sqrt_disc) / (2 * a)
#         t2 = (-b + sqrt_disc) / (2 * a)
#         t_candidates = [t1, t2]

#         # Step 3: Filter t-values to find valid intersections within cylinder height
#         valid_t = []
#         for t in t_candidates:
#             if t < 0:
#                 continue
#             y = O[1] + t * D[1]
#             if self.base_center[1] <= y <= self.base_center[1] + self.height:
#                 valid_t.append(t)

#         # Step 4

#         if valid_t.empty():
#             return None
        
#         return valid_t
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
        self.position = Vector(position[0], position[1], position[2])


class DirectionalLight(Light):
    """Directional light with a specified direction vector."""
    def __init__(self, intensity: float, direction: Vector):
        super().__init__(type_="directional", intensity=intensity)
        if not (isinstance(direction, (list, tuple)) and len(direction) == 3):
            raise TypeError("Direction must be a 3-element tuple or list.")
        self.direction = Vector(direction[0], direction[1], direction[2])
