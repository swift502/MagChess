# Chessboard is the game state detector and primary app manager
# Based on sensor values, this class has to infer where all the pieces are, and call ui updates accordingly
# It also communicates with stockfish and hands analysis information over to ui
# Basically it's a three way bridge between sensors, stockfish and the ui

import asyncio
import flet as ft

from constants import SENSOR_THRESHOLD_HIGH, SENSOR_THRESHOLD_LOW
from utilities import inverse_lerp, lerp, lerp_three
from sensors import SWSensors
from ui_instance import MagChessUI

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

        if self.smooth_value < SENSOR_THRESHOLD_LOW:
            self.sensor_indicator.border.top.color = "#ff0000"
        elif self.smooth_value > SENSOR_THRESHOLD_HIGH:
            self.sensor_indicator.border.top.color = "#00ffff"
        else:
            self.sensor_indicator.border.top.color = "#000000"

        factor = inverse_lerp(raw, SENSOR_THRESHOLD_LOW, SENSOR_THRESHOLD_HIGH)
        self.sensor_indicator.bgcolor = lerp_three("#ff0000", "#000000", "#00ffff", factor)

class Chessboard:

    squares: dict[tuple[int, int], Square]

    def __init__(self, page: ft.Page, ui: MagChessUI, sensors: SWSensors):
        self.page = page
        self.ui = ui
        self.sensors = sensors

        self.squares = {}
        for letter in range(8):
            for number in range(8):
                self.squares[(letter, number)] = Square(letter, number, ui)
        
        page.run_task(self.update)

    async def update(self):
        while True:

            raw = self.sensors.get_value_array()
            for pos, square in self.squares.items():
                square.update(raw[pos])

                
            self.page.update()

            await asyncio.sleep(1/60)
