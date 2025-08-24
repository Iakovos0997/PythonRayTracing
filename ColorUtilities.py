def scale_rgb(color, scalar):
    """
    Multiply an RGB tuple by a scalar and clamp each value to 255.

    Args:
        color: tuple of 3 integers (R, G, B)
        scalar: numeric multiplier

    Returns:
        tuple of 3 integers (R, G, B) scaled and clamped to 255
    """
    if not isinstance(color, tuple) or len(color) != 3:
        raise ValueError("Color must be a tuple of 3 integers (R, G, B).")
    if not all(isinstance(c, (int, float)) for c in color):
        raise TypeError("Each color component must be int or float.")
    if not isinstance(scalar, (int, float)):
        raise TypeError("Scalar must be numeric.")

    return tuple(min(255, max(0, int(round(c * scalar)))) for c in color)

def rgb_to_hex(color):
    return "#%02x%02x%02x" % color