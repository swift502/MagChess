from pathlib import Path

import chess

def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: tuple[int, ...]):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def lerp_rgb(c1: tuple[int, ...], c2: tuple[int, ...], t: float):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def lerp_hex(hex1: str, hex2: str, t: float):
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
    lerped_rgb = lerp_rgb(rgb1, rgb2, t)
    return rgb_to_hex(lerped_rgb)

def lerp_hex_three(a_hex: str, b_hex: str, c_hex: str, factor: float):
    a, b, c = map(hex_to_rgb, (a_hex, b_hex, c_hex))

    if factor <= 0.5:
        t = factor / 0.5
        return rgb_to_hex(lerp_rgb(a, b, t))
    else:
        t = (factor - 0.5) / 0.5
        return rgb_to_hex(lerp_rgb(b, c, t))

def lerp(a: float, b: float, t: float) -> float:
    t = max(0.0, min(1.0, t))
    return (1.0 - t) * a + t * b

def inverse_lerp(a: float, b: float, value: float):
    if a == b:
        return 0.0
    t = (value - a) / (b - a)
    return max(0.0, min(1.0, t))

def asset_path(path: str) -> str:
    return str(Path(__file__).parent / "assets" / path)

def data_path(path: str) -> str:
    return str(Path(__file__).parent / "data" / path)

def color_format(color: chess.Color | None):
    match color:
        case chess.WHITE:
            return "White"
        case chess.BLACK:
            return "Black"
        case None:
            return "Draw"