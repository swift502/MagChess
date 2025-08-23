import flet as ft

from ui_instance import MagChessUI
from constants import SENSOR_THRESHOLD_HIGH, SENSOR_THRESHOLD_LOW
from utilities import inverse_lerp, lerp, lerp_hex

class Square:

    sensor_indicator: ft.Container
    smooth_value: float

    def __init__(self, letter: int, number: int, ui: MagChessUI):
        self.letter = letter
        self.number = number
        self.sensor_indicator = ui.sensor_indicators[(letter, number)]
        self.smooth_value = 0.0
    
    def update(self, raw):
        self.smooth_value = lerp(self.smooth_value, raw, 0.1)

        assert self.sensor_indicator.border is not None
        assert self.sensor_indicator.border.top is not None

        if self.smooth_value < SENSOR_THRESHOLD_LOW:
            self.sensor_indicator.border.top.color = "#000000"
        elif self.smooth_value > SENSOR_THRESHOLD_HIGH:
            self.sensor_indicator.border.top.color = "#ffffff"
        else:
            self.sensor_indicator.border.top.color = "#888888"

        factor = inverse_lerp(raw, SENSOR_THRESHOLD_LOW, SENSOR_THRESHOLD_HIGH)
        self.sensor_indicator.bgcolor = lerp_hex("#000000", "#ffffff", factor)