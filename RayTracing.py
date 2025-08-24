from graphics import GraphWin
from SceneObjects import Scene
from VectorUtilities import Vector
from ColorUtilities import scale_rgb, rgb_to_hex
from concurrent.futures import ThreadPoolExecutor

# ---------- Ray Tracer Core ----------

def canvas_to_viewport(x: float, y: float, Vw: float, Vh: float, d: float, Cw: int, Ch: int) -> tuple:
    """Convert canvas coordinates to viewport coordinates."""
    return Vector(x * Vw / Cw, y * Vh / Ch, d)


def trace_ray(
    origin: Vector,
    direction: Vector,
    t_min: float,
    t_max: float,
    scene: Scene,
    background=(255, 255, 255)
) -> tuple:
    """
    Trace a ray from the camera through the scene and return the color.
    """
    closest_t = float('inf')
    closest_obj = None

    # Find nearest intersection
    for obj in scene.objects:
        intersections = obj.intersect(origin, direction)
        if intersections is None:
            continue
        for t in intersections:
            if t_min <= t <= t_max and t < closest_t:
                closest_t = t
                closest_obj = obj

    if closest_obj is None:
        return background

    # Compute intersection and normal
    P = origin + direction * closest_t
    N = (P - closest_obj.center).normalize()
    V = -direction  # Direction towards camera

    # Compute lighting (diffuse + specular)
    intensity = compute_lighting(P, N, scene, V, closest_obj.specular)

    # Scale color
    return scale_rgb(closest_obj.color, intensity)


def compute_lighting(P: Vector, N: Vector, scene: Scene, V: Vector, s: int) -> float:
    """
    Compute the lighting intensity at a point with normal N and view vector V.
    Includes ambient, diffuse, and specular components.
    """
    intensity = 0.0

    for light in scene.lights:
        if light.type == "ambient":
            intensity += light.intensity
            continue

        # Determine light direction
        if light.type == "point":
            L = (light.position - P).normalize()
        else:  # directional
            L = light.direction.normalize()

        # Diffuse component
        n_dot_l = N.dot(L)
        if n_dot_l > 0:
            intensity += light.intensity * n_dot_l

        # Specular component
        if s != -1:
            R = N * (2 * n_dot_l) - L
            r_dot_v = R.dot(V)
            if r_dot_v > 0:
                intensity += light.intensity * (r_dot_v ** s)

    return min(1.0, intensity)  # Clamp to 1.0


# ---------- Renderer ----------

def render_row(y: int, width: int, height: int, origin: tuple, Vw: float, Vh: float, d: float, scene: Scene) -> tuple:
    """
    Render a single row of pixels and return the list of color hex values.
    """
    row_colors = []
    y_canvas = height / 2 - y

    for x in range(width):
        x_canvas = x - width / 2
        direction = canvas_to_viewport(x_canvas, y_canvas, Vw, Vh, d, width, height).normalize()
        color = trace_ray(origin, direction, 1.0, float('inf'), scene)
        row_colors.append(rgb_to_hex(color))

    return (y, row_colors)


def render_parallel_rows(win: GraphWin, width: int, height: int, scene: Scene, max_workers: int = 8):
    """Render the scene using parallel row processing."""
    origin = Vector(0, 0, 0)
    Vw, Vh, d = 1.0, 1.0, 1.0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(render_row, y, width, height, origin, Vw, Vh, d, scene) for y in range(height)]
        for future in futures:
            y, row_colors = future.result()
            for x, color_hex in enumerate(row_colors):
                win.plot(x, y, color_hex)


def render_sequential(win: GraphWin, width: int, height: int, scene: Scene):
    """Sequential renderer for testing or small images."""
    origin = Vector(0, 0, 0)
    Vw, Vh, d = 1.0, 1.0, 1.0

    for y in range(height):
        y_canvas = height / 2 - y
        for x in range(width):
            x_canvas = x - width / 2
            direction = canvas_to_viewport(x_canvas, y_canvas, Vw, Vh, d, width, height).normalize()
            color = trace_ray(origin, direction, 1.0, float('inf'), scene)
            win.plot(x, y, rgb_to_hex(color))
