from graphics import *
from SceneObjects import *
from VectorUtilities import *
from ColorUtilities import *
from RayTracing import *


def main():
    width, height = 400, 400
    win = GraphWin("Object-Agnostic Raytracer", width, height, autoflush=False)

    objects = [
        Sphere(Vector(0, -1, 3), 1, (255, 0, 0), 500),   # Red
        Sphere(Vector(2,  0, 4), 1, (0, 0, 255), 500),   # Blue
        Sphere(Vector(-2, 0, 4), 1, (0, 255, 0), 10),   # Green,
        Sphere(Vector(0, -5001, 0), 5000, (255, 255, 0), 1000) # Yellow
    ]

    lights = [
        AmbientLight(intensity=0.2),
        PointLight(intensity=0.6, position=(2, 1, 0)),
        DirectionalLight(intensity=0.2, direction=(1,4,4))
    ]

    scene = Scene(objects, lights)

    render_parallel_rows(win, width, height, scene, max_workers=8)
    win.getMouse()
    win.close()

if __name__ == "__main__":
    main()
