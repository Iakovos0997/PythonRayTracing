import math

Cw, Ch = 10, 10
d = 1
Vw, Vh = 1, 1
O = (0, 0, 0)
inf = math.inf


def CanvasToViewport(x, y):
    return (x * Vw / Cw, y * Vh / Ch, d)

def TraceRay(O, D, t_min, t_max):
    closest_t = inf
    closest_sphere = None
    for sphere in scene.spheres:
        t1, t2 = IntersectRaySphere(O, D, sphere)
        if t1 in [t_min, t_max] and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere
        if t2 in [t_min, t_max] and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere
    if closest_sphere == None:
        return BACKGROUND_COLOR
    return closest_sphere.color

def IntersectRaySphere(O, D, sphere):
    r = sphere.radio
    CO = O - sphere.center
   
    a = dot(D, D)
    b = 2*dot(CO, D)
    c = dot(CO, CO) - r*r
   
    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return inf, inf
   
    t1 = (-b + sqrt(discriminante)) // (2*a)
    t2 = (-b - sqrt(discriminante)) // (2*a)

    return t1, t2


for x in range (-Cw//2, Cw//2):
    for y in range(-Ch//2, Ch//2):
        D = CanvasToViewport(x, y)
        color = TraceRay(O, D, 1, inf)
        canvas.PutPixel(x, y, color) 