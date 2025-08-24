from graphics import *
import math

# ---------- Ray Tracer Core ----------

def dot(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def canvas_to_viewport(x, y, Vw, Vh, d, Cw, Ch):
    return (x * Vw / Cw, y * Vh / Ch, d)

def rgb_to_hex(color):
    return "#%02x%02x%02x" % color

def trace_ray(O, D, t_min, t_max, objects, background=(255,255,255)):
    closest_t = float('inf')
    closest_obj = None

    for obj in objects:
        ts = obj.intersect(O, D)   # object defines its own intersection
        if ts is None:
            continue
        for t in ts:
            if t_min <= t <= t_max and t < closest_t:
                closest_t = t
                closest_obj = obj

    if closest_obj is None:
        return background
    return closest_obj.color

# ---------- Object Abstractions ----------

class SceneObject:
    """Base class: requires intersect(O, D) and color"""
    def __init__(self, color):
        self.color = color
    def intersect(self, O, D):
        raise NotImplementedError("Subclass must implement intersect")

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

# ---------- Renderer ----------

def render(win, width, height, objects):
    O = (0,0,0)
    Vw, Vh, d = 1.0, 1.0, 1.0
    for y_img in range(height):
        y = (height/2 - y_img)
        for x_img in range(width):
            x = x_img - width/2
            D = canvas_to_viewport(x, y, Vw, Vh, d, width, height)
            color = trace_ray(O, D, 1.0, float('inf'), objects)
            win.plot(x_img, y_img, rgb_to_hex(color))

# ---------- Example Usage ----------

def main():
    width, height = 400, 400
    win = GraphWin("Object-Agnostic Raytracer", width, height, autoflush=False)

    objects = [
        Sphere((0, -1, 3), 1, (255, 0, 0)),   # Red
        Sphere((2,  0, 4), 1, (0, 0, 255)),   # Blue
        Sphere((-2, 0, 4), 1, (0, 255, 0)),   # Green
    ]

    render(win, width, height, objects)
    win.getMouse()
    win.close()

if __name__ == "__main__":
    main()
