import chess
import flet as ft

from constants import SENSOR_THRESHOLD_HIGH, SENSOR_THRESHOLD_LOW
from ui_instance import MagChessUI
from utilities import inverse_lerp, lerp, lerp_hex

class Cell:
    sensor_indicator: ft.Container
    smooth_value: float
    state: int

    def __init__(self, co_letter: int, co_number: int, ui: MagChessUI):
        self.sensor_indicator = ui.sensor_indicators[(co_letter, co_number)]
        self.smooth_value = 0.0
    
    def update(self, raw):
        # Value
        self.smooth_value = lerp(self.smooth_value, raw, 0.1)

        # State
        if self.smooth_value < SENSOR_THRESHOLD_LOW:
            self.state = -1
            self.sensor_indicator.border.top.color = "#000000"
        elif self.smooth_value > SENSOR_THRESHOLD_HIGH:
            self.state = 1
            self.sensor_indicator.border.top.color = "#ffffff"
        else:
            self.state = 0
            self.sensor_indicator.border.top.color = "#888888"

        # Raw sensor value
        factor = inverse_lerp(SENSOR_THRESHOLD_LOW, SENSOR_THRESHOLD_HIGH, raw)
        self.sensor_indicator.bgcolor = lerp_hex("#000000", "#ffffff", factor)

    @property
    def state_format(self):
        if self.state == -1:
            return 'B'
        elif self.state == 1:
            return 'W'
        else:
            return '.'
    
    @property
    def color(self):
        if self.state == -1:
            return chess.BLACK
        elif self.state == 1:
            return chess.WHITE
        else:
            return None