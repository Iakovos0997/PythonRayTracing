from graphics import GraphWin
from SceneObjects import Scene
from VectorUtilities import Vector
from ColorUtilities import scale_rgb, rgb_to_hex
from concurrent.futures import ThreadPoolExecutor

# ---------- Ray Tracer Core ----------

def canvas_to_viewport(x: float, y: float, Vw: float, Vh: float, d: float, Cw: int, Ch: int) -> tuple:
    """Convert canvas coordinates to viewport coordinates."""
    return Vector(x * Vw / Cw, y * Vh / Ch, d)


MAX_DEPTH = 3  # maximum recursion depth

def reflect(D: Vector, N: Vector) -> Vector:
    """Reflect direction D around normal N."""
    return D - N * 2 * D.dot(N)


def trace_ray(O: Vector, D: Vector, t_min: float, t_max: float, scene: Scene, depth: int = 0) -> tuple:
    """
    Trace a ray from origin O along direction D through the scene.
    Returns an RGB color tuple.
    Supports diffuse, specular, and reflective surfaces.
    """
    if depth > MAX_DEPTH:
        return (0, 0, 0)  # background for deep recursion

    # Find closest intersection
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
        return (255, 255, 255)  # background color

    # Intersection point
    P = O + D * closest_t
    # Surface normal
    N = closest_obj.normal_at(P)
    # View vector (towards camera)
    V = -D
    # Local lighting (diffuse + specular)
    intensity = ComputeLighting(P, N, scene, V, closest_obj.specular)
    local_color = scale_rgb(closest_obj.color, intensity)

    # Handle reflection
    reflective = getattr(closest_obj, "reflective", 0.0)
    if reflective > 0:
        R = reflect(D, N).normalize()
        # Small offset to avoid self-intersection
        epsilon = 1e-4
        reflected_color = trace_ray(P + R * epsilon, R, t_min, t_max, scene, depth + 1)
        # Mix colors
        local_color = tuple(
            int(local_color[i] * (1 - reflective) + reflected_color[i] * reflective)
            for i in range(3)
        )

    return local_color


def ComputeLighting(P: Vector, N: Vector, scene: Scene, V: Vector, s: int) -> float:
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

from concurrent.futures import ProcessPoolExecutor, as_completed

def render_parallel_rows(win: GraphWin, width: int, height: int, scene: Scene, max_workers: int = None):
    """Render the scene using parallel row processing (compute first, draw later)."""
    origin = Vector(0, 0, 0)
    Vw, Vh, d = 1.0, 1.0, 1.0

    row_results = [None] * height  # preallocate buffer for rows

    # Phase 1: parallel computation
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(render_row, y, width, height, origin, Vw, Vh, d, scene): y for y in range(height)}

        for future in as_completed(futures):
            y, row_colors = future.result()
            row_results[y] = row_colors  # store in buffer at correct index

    # Phase 2: sequential drawing
    for y, row_colors in enumerate(row_results):
        for x, color_hex in enumerate(row_colors):
            win.plot(x, y, color_hex)
