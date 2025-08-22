# Chessboard is the game state detector and primary app manager
# Based on sensor values, this class has to infer where all the pieces are, and call ui updates accordingly
# It also communicates with stockfish and hands analysis information over to ui
# Basically it's a three way bridge between sensors, stockfish and the ui

import asyncio
import flet as ft

from sensors import SWSensors
from ui_instance import MagChessUI

class Chessboard:
    def __init__(self, page: ft.Page, ui: MagChessUI, sensors: SWSensors):
        self.page = page
        self.ui = ui
        self.sensors = sensors
        
        page.run_task(self.update)

    async def update(self):
        while True:

            # self.ui.update_sensors(self.sensors.get_value_array())

            await asyncio.sleep(1/60)
