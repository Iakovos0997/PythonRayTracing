# Object-Agnostic Ray Tracer

This project is a Python ray tracer designed to render 3D scenes with spheres, cylinders, and planes, supporting diffuse and specular lighting. The code is modular, object-agnostic, and designed for educational purposes, demonstrating core ray tracing concepts and lighting models.

---

## Table of Contents

* [Features](#features)
* [Project Structure](#project-structure)
* [Vector Utilities](#vector-utilities)
* [Scene Objects](#scene-objects)
* [Lighting](#lighting)
* [Ray Tracing Core](#ray-tracing-core)
* [Rendering](#rendering)
* [Extending the Ray Tracer](#extending-the-ray-tracer)
* [Usage](#usage)

---

## Features

* Object-agnostic design: Each object (sphere, cylinder, plane) defines its own `intersect` and `normal_at` methods.
* Diffuse and specular lighting using ambient, point, and directional lights.
* Parallel rendering using Python’s `ThreadPoolExecutor`.
* Random scene generation support for multiple objects and lights.
* Vector class with `x`, `y`, `z` attributes for clarity.
* RGB utilities for scaling colors and converting to hex for rendering.

---

## Project Structure

```
project_root/
│
├─ main.py                   # Main script: creates scene and renders
├─ SceneObjects.py           # SceneObject, Sphere, Cylinder, Plane classes
├─ VectorUtilities.py        # Vector class and vector math functions
├─ ColorUtilities.py         # Color helpers (scale_rgb, rgb_to_hex)
├─ lights.py                 # Light classes: Ambient, Point, Directional
├─ graphics/                 # graphics.py library
└─ README.md                 # Project documentation
```

---

## Vector Utilities

`VectorUtilities.py` provides:

* `Vector` class: supports `x`, `y`, `z`, vector arithmetic, length, normalization, opposite.
* Functions: `dot`, `add`, `sub`, `mul_scalar`, `length`, `normalize`, `opposite`.
* Validation for vector operations to ensure numeric types and matching dimensions.

Example:

```python
v1 = Vector(1, 2, 3)
v2 = Vector(4, 0, 1)
v3 = v1 + v2  # Vector addition
```

---

## Scene Objects

### Base Class: `SceneObject`

* Attributes: `color`, `specular`, `axis`.
* Abstract methods:

  * `intersect(O, D)`: returns intersection points along a ray.
  * `normal_at(P)`: returns surface normal at point `P`.

### Sphere

* Defined by `center` and `radius`.
* Implements `intersect` using quadratic formula.
* Computes normal with `normal_at`.

### Cylinder

* Defined by `base_center`, `axis`, `radius`, `height`.
* Supports arbitrary orientation via `axis` vector.
* `intersect` solves cylinder equation in 3D space, clips to caps.
* `normal_at` accounts for side surface and caps.

### Plane

* Defined by a `point` and a `normal` (via `axis`).
* `intersect` solves ray-plane equation.
* `normal_at` returns plane normal (constant).
* Axis allows orientation control (e.g., diagonal walls).

---

## Lighting

* **AmbientLight**: adds constant illumination.
* **PointLight**: emits light from a position in all directions.
* **DirectionalLight**: light from a fixed direction (like the sun).

Lighting computation:

```python
intensity = ambient + sum(diffuse + specular)
```

* Diffuse: based on angle between light vector `L` and surface normal `N`.
* Specular: based on angle between reflected vector `R` and viewer `V`.

---

## Ray Tracing Core

* `trace_ray(O, D, t_min, t_max, scene)`:

  * Finds closest object intersected by ray `O + t*D`.
  * Computes intersection `P` and normal `N`.
  * Computes lighting intensity and scales object color.

* Supports specular reflection via object’s `specular` attribute.

---

## Rendering

* `render_parallel_rows(win, width, height, scene)`:

  * Uses multithreading for faster rendering by computing rows in parallel.
* Converts 3D coordinates to 2D viewport using `canvas_to_viewport`.
* Uses `rgb_to_hex` to plot colors in `graphics.py` window.

---

## Extending the Ray Tracer

To add a new object:

1. Create a class inheriting from `SceneObject`.
2. Implement:

   * `intersect(O, D)` → return valid t values along ray.
   * `normal_at(P)` → return surface normal at point `P`.
3. Add `specular` and `axis` attributes if needed.
4. Add instance to `scene.objects`.

To add a new light type:

1. Create a class inheriting from `Light`.
2. Implement any additional attributes (position, direction).
3. Add instance to `scene.lights`.

---

## Usage Example

```python
from graphics import GraphWin
from SceneObjects import Sphere, Cylinder, Plane, Scene
from lights import AmbientLight, PointLight, DirectionalLight
from RayTracer import render_parallel_rows

win = GraphWin("Ray Tracer", 800, 600, autoflush=False)

objects = [
    Sphere(center=Vector(0, -1, 3), radius=1, color=(255,0,0)),
    Cylinder(base_center=Vector(-2,0,3), axis=Vector(1,0,0), radius=0.5, height=2, color=(255,0,255)),
    Plane(point=Vector(0,0,5), axis=Vector(1,0,1), color=(200,200,200))
]

lights = [
    AmbientLight(0.2),
    PointLight(0.6, position=Vector(2,1,0)),
    DirectionalLight(0.2, direction=Vector(1,4,4))
]

scene = Scene(objects, lights)
render_parallel_rows(win, 800, 600, scene, max_workers=8)
win.getMouse()
win.close()
```

---

This README now documents:

* Project purpose and features.
* File structure.
* Vector math and object abstractions.
* Lights, diffuse, and specular shading.
* Adding new objects and lights.
* Example usage.
