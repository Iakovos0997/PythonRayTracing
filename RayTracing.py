from graphics import *
import math
from SceneObjects import *
from VectorUtilities import *
from ColorUtilities import *

# ---------- Ray Tracer Core ----------

def canvas_to_viewport(x, y, Vw, Vh, d, Cw, Ch):
    return (x * Vw / Cw, y * Vh / Ch, d)

def trace_ray(O, D, t_min, t_max, scene, background=(255,255,255)):
    closest_t = float('inf')
    closest_obj = None

    for obj in scene.objects:
        ts = obj.intersect(O, D)
        if ts is None:
            continue
        for t in ts:
            if t_min <= t <= t_max and t < closest_t:
                closest_t = t
                closest_obj = obj

    if closest_obj is None:
        return background

    # Intersection point
    P = add(O, mul_scalar(D, closest_t))
    # Surface normal
    N = normalize(sub(P, closest_obj.center))
    # Diffuse lighting
    intensity = ComputeLighting(P, N, scene, opposite(D), closest_obj.specular)
    # Scale color
    return scale_rgb(closest_obj.color, intensity)

def ComputeLighting(P, N, scene, V, s):
    """Compute diffuse lighting at point P with normal N"""
    intensity = 0.0
    for light in scene.lights:
        if light.type == "ambient":
            intensity += light.intensity
        else:
            if light.type == "point":
                L = normalize(sub(light.position, P))
            else:  # directional
                L = normalize(light.direction)

            # Difuse shading
            n_dot_l = dot(N, L)
            if n_dot_l > 0:
                intensity += light.intensity * n_dot_l

            # Specular shading
            if s != -1:
                R = sub(mul_scalar(N, 2 * dot(N, L)), L)
                r_dot_v = dot(R, V)
                if r_dot_v > 0:
                    intensity += light.intensity * (r_dot_v ** s)

    return min(1.0, intensity)  # clamp to 1.0

# ---------- Renderer ----------

from concurrent.futures import ThreadPoolExecutor

def render_row(y_img, width, height, O, Vw, Vh, d, scene):
    row_colors = []
    y = height/2 - y_img
    for x_img in range(width):
        x = x_img - width/2
        D = normalize(canvas_to_viewport(x, y, Vw, Vh, d, width, height))
        color = trace_ray(O, D, 1.0, float('inf'), scene)
        row_colors.append(rgb_to_hex(color))
    return (y_img, row_colors)

def render_parallel_rows(win:GraphWin, width:int, height:int, scene:Scene, max_workers=8):
    O = (0,0,0)
    Vw, Vh, d = 1.0, 1.0, 1.0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(render_row, y, width, height, O, Vw, Vh, d, scene) for y in range(height)]

        for future in futures:
            y_img, row_colors = future.result()
            for x_img, color_hex in enumerate(row_colors):
                win.plot(x_img, y_img, color_hex)



def render(win:GraphWin, width:int, height:int, scene:Scene):
    O = (0,0,0)
    Vw, Vh, d = 1.0, 1.0, 1.0
    for y_img in range(height):
        y = (height/2 - y_img)
        for x_img in range(width):
            x = x_img - width/2
            D = canvas_to_viewport(x, y, Vw, Vh, d, width, height)
            color = trace_ray(O, D, 1.0, float('inf'), scene)
            win.plot(x_img, y_img, rgb_to_hex(color))