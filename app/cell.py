import chess
import flet as ft

from constants import SENSOR_CALIBRATION_DATA, SENSOR_TRIGGER_DELTA
from ui_instance import MagChessUI
from utilities import inverse_lerp, lerp_hex

class Cell:
    sensor_indicator: ft.Container
    detected_color: chess.Color | None

    def __init__(self, coords: tuple[int, int], ui: MagChessUI):
        self.coords = coords
        self.detected_color = None

        self.ref_value = SENSOR_CALIBRATION_DATA[str(coords)]
        self.threshold_low = self.ref_value - SENSOR_TRIGGER_DELTA
        self.threshold_high = self.ref_value + SENSOR_TRIGGER_DELTA
        self.sensor_indicator = ui.sensor_indicators[coords]

    def update(self, sensor_value: float):
        # State
        if sensor_value < self.threshold_low:
            self.detected_color = chess.WHITE
            self.sensor_indicator.border.top.color = "#ffffff"
        elif sensor_value > self.threshold_high:
            self.detected_color = chess.BLACK
            self.sensor_indicator.border.top.color = "#000000"
        else:
            self.detected_color = None
            self.sensor_indicator.border.top.color = "#888888"

        # Ui
        factor = inverse_lerp(self.threshold_low, self.threshold_high, sensor_value)
        self.sensor_indicator.bgcolor = lerp_hex("#ffffff", "#000000", factor)

    @property
    def state_format(self):
        if self.detected_color == chess.BLACK:
            return 'B'
        elif self.detected_color == chess.WHITE:
            return 'W'
        else:
            return '.'
    