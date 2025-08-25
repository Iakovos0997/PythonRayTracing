from graphics import *
from SceneObjects import *
from VectorUtilities import *
from ColorUtilities import *
from RayTracing import *
import pickle


def make_objects():
    """Create and return the objects in the scene."""
    return [
        # Central spheres
        Sphere(Vector(0, -1, 3), 1, (255, 0, 0), 500,   reflective=0.1),    # Red
        Sphere(Vector(2,  0, 4), 1, (0, 0, 255), 500,   reflective=0.1),    # Blue
        Sphere(Vector(-2, 0, 4), 1, (0, 255, 0), 10,    reflective=0.1),     # Green
        # Sphere(Vector(0, 1.5, 2.5), 0.7, (255, 255, 0), 100),  # Yellow floating sphere

        # Magenta cylinder (angled)
        Cylinder(
            base_center=Vector(-1, 3, 7),
            axis=Vector(1, -1, 1),
            radius=0.5,
            height=4,
            color=(255, 0, 255),
            specular=500
        ),

        # Floor plane
        Plane(
            point=Vector(0, -2, 0),
            normal=Vector(0, 1, 0),
            color=(200, 200, 200),
            specular=100,
            axis=Vector(0, 1, 0)
        ),

        # Back wall plane (mirror-like effect)
        Plane(
            point=Vector(0, 0, 13),
            normal=Vector(0, 0, -1),
            color=(180, 180, 200),   # bluish-gray
            specular=500,
            axis=Vector(0, 0, -1),
            reflective=0.8
        ),

        # Floating torus
        Torus(
            center=Vector(0, 2.5, 7),
            major_radius=1.5,
            minor_radius=0.5,
            color=(0, 255, 255),
            specular=300,
            axis=Vector(1, -1, 1)
        )
    ]


def make_lights():
    """Create and return the lights in the scene."""
    return [
        AmbientLight(intensity=0.2),
        PointLight(intensity=0.6, position=(2, 3, -2)),   # warmer overhead light
        DirectionalLight(intensity=0.2, direction=(1, 4, 4))
    ]


def main():
    width, height = 600, 600
    win = GraphWin("Object-Agnostic Raytracer", width, height, autoflush=False)

    # Build scene
    objects = make_objects()
    lights = make_lights()
    scene = Scene(objects, lights)

    # Render scene
    render_parallel_rows(win, width, height, scene, max_workers=12)

    # Wait for user
    win.getMouse()
    win.close()


if __name__ == "__main__":
    main()
