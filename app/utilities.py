def hex_to_rgb(hex_color):
    """Convert hex color (#RRGGBB) to RGB tuple (r,g,b)."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple (r,g,b) to hex color (#RRGGBB)."""
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def lerp_color(c1, c2, t):
    """Linear interpolate between two RGB colors."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def lerp_hex(hex1, hex2, t):
    """Linear interpolate between two hex colors."""
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
    lerped_rgb = lerp_color(rgb1, rgb2, t)
    return rgb_to_hex(lerped_rgb)

def lerp_hex_three(a, b, c, factor):
    """
    Lerp between three hex colors.
    a at factor 0.0
    b at factor 0.5
    c at factor 1.0
    """
    a, b, c = map(hex_to_rgb, (a, b, c))

    if factor <= 0.5:
        # scale to [0,1] for a→b
        t = factor / 0.5
        return rgb_to_hex(lerp_color(a, b, t))
    else:
        # scale to [0,1] for b→c
        t = (factor - 0.5) / 0.5
        return rgb_to_hex(lerp_color(b, c, t))

def lerp(a: float, b: float, t: float) -> float:
    """Linearly interpolate between a and b with t clamped to [0, 1]."""
    t = max(0.0, min(1.0, t))
    return (1.0 - t) * a + t * b

def inverse_lerp(x, a, b):
    """
    Inverse linear interpolation with clamping.
    Returns t in [0,1] such that lerp(a, b, t) ≈ x.
    """
    if a == b:
        return 0.0  # avoid division by zero
    t = (x - a) / (b - a)
    return max(0.0, min(1.0, t))
