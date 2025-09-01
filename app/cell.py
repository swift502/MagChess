import chess
import flet as ft

from constants import SENSOR_CALIBRATION_DATA, SENSOR_TRIGGER_DELTA
from ui_instance import MagChessUI
from utilities import inverse_lerp, lerp_hex

class Cell:
    sensor_indicator: ft.Container
    # smooth_value: float
    state: int

    def __init__(self, coords: tuple[int, int], ui: MagChessUI):
        self.coords = coords
        # self.smooth_value = 0.0
        self.state = 0

        self.ref_value = SENSOR_CALIBRATION_DATA[str(coords)]
        self.threshold_low = self.ref_value - SENSOR_TRIGGER_DELTA
        self.threshold_high = self.ref_value + SENSOR_TRIGGER_DELTA
        self.sensor_indicator = ui.sensor_indicators[coords]

    def update(self, sensor_value: float):
        # Value
        # self.smooth_value = lerp(self.smooth_value, sensor_value, 0.1)

        # State
        if sensor_value < self.threshold_low:
            self.state = 1
            self.sensor_indicator.border.top.color = "#ffffff"
        elif sensor_value > self.threshold_high:
            self.state = -1
            self.sensor_indicator.border.top.color = "#000000"
        else:
            self.state = 0
            self.sensor_indicator.border.top.color = "#888888"

        # Raw sensor value
        factor = inverse_lerp(self.threshold_low, self.threshold_high, sensor_value)
        self.sensor_indicator.bgcolor = lerp_hex("#ffffff", "#000000", factor)

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