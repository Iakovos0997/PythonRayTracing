import math
from VectorUtilities import *

class Scene:
    def __init__(self, objects, lights):
        self.objects = objects
        self.lights = lights

class SceneObject:
    """Base class: requires intersect(O, D) and color"""
    def __init__(self, color):
        self.color = color
    def intersect(self, O, D):
        raise NotImplementedError("Subclass must implement intersect")

# ------------- Spheres -------------------

class Sphere(SceneObject):
    def __init__(self, center, radius, color):
        super().__init__(color)
        self.center = center
        self.radius = radius

    def intersect(self, O, D):
        CO = sub(O, self.center)
        a = dot(D, D)
        b = 2 * dot(CO, D)
        c = dot(CO, CO) - self.radius**2
        discriminant = b*b - 4*a*c
        if discriminant < 0:
            return None
        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b + sqrt_disc) / (2*a)
        t2 = (-b - sqrt_disc) / (2*a)
        return (t1, t2)

# ------------- Lights -------------------
class Light:
    def __init__(self, type:str, intensity:float):
        self.type = type
        self.intensity = intensity

class AmbientLight(Light):
    def __init__(self, intensity:float):
        super().__init__(type="ambient", intensity=intensity)

class PointLight(Light):
    def __init__(self, intensity:float, position:tuple):
        super().__init__(type="point", intensity=intensity)
        self.position = position

class DirectionalLight(Light):
    def __init__(self, intensity:float, direction:tuple):
        super().__init__(type="directional", intensity=intensity)
        self.direction = direction