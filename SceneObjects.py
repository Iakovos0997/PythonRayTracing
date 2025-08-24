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
    
    def normal_at(self, P: Vector) -> Vector:
        raise NotImplementedError("Subclasses must implement the normal_at method.")


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
    
    def normal_at(self, P: Vector) -> Vector:
        # Vector from center to P, normalized
        return (P - self.center).normalize()

class Cylinder(SceneObject):
    def __init__(
        self,
        base_center: Vector,
        axis: Vector = Vector(0,1,0),
        radius: float = 1.0,
        height: float = 1.0,
        color: Tuple[int, int, int] = (255, 0, 0),
        specular: int = 500
    ):
        super().__init__(color)
        self.base_center = base_center
        self.axis = axis.normalize()
        self.radius = radius
        self.height = height
        self.specular = specular

    def intersect(self, O, D):
        """
        Intersect ray O + t*D with cylinder (including caps).
        Returns tuple of valid t values or None.
        """
        axis = self.axis
        CO = O - self.base_center

        # Project D and CO onto plane perpendicular to axis
        D_proj = D - axis * D.dot(axis)
        CO_proj = CO - axis * CO.dot(axis)

        a = D_proj.dot(D_proj)
        b = 2 * D_proj.dot(CO_proj)
        c = CO_proj.dot(CO_proj) - self.radius**2

        t_side = []
        disc = b*b - 4*a*c
        if disc >= 0:
            sqrt_disc = math.sqrt(disc)
            for t in [(-b - sqrt_disc) / (2*a), (-b + sqrt_disc) / (2*a)]:
                P = O + D * t
                h = (P - self.base_center).dot(axis)
                if 0 <= h <= self.height:
                    t_side.append(t)

        # Check caps
        t_caps = []
        for cap_h, cap_normal in [(0, -axis), (self.height, axis)]:
            denom = D.dot(cap_normal)
            if abs(denom) > 1e-6:
                t = ((self.base_center + axis*cap_h) - O).dot(cap_normal) / denom
                if t > 0:
                    P = O + D * t
                    # check if within radius
                    if (P - (self.base_center + axis*cap_h) - axis*0).length() <= self.radius:
                        t_caps.append(t)

        t_all = t_side + t_caps
        if not t_all:
            return None
        return tuple(sorted(t_all))

    def normal_at(self, P):
        AP = P - self.base_center
        h = AP.dot(self.axis)

        if abs(h) < 1e-6:  # bottom cap
            return -self.axis
        elif abs(h - self.height) < 1e-6:  # top cap
            return self.axis
        else:
            axis_point = self.base_center + self.axis * h
            return (P - axis_point).normalize()

    
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
