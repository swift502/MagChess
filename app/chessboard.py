# Chessboard is the game state detector and primary app manager
# Based on sensor values, this class has to infer where all the pieces are, and call ui updates accordingly
# It also communicates with stockfish and hands analysis information over to ui
# Basically it's a three way bridge between sensors, stockfish and the ui

import asyncio
import flet as ft

from sensors import SWSensors
from ui_instance import MagChessUI
from cell import Cell

class Chessboard:

    cells: dict[tuple[int, int], Cell]

    def __init__(self, page: ft.Page, ui: MagChessUI, sensors: SWSensors):
        self.page = page
        self.ui = ui
        self.sensors = sensors

        self.cells = {}
        for co_letter in range(8):
            for co_number in range(8):
                self.cells[(co_letter, co_number)] = Cell(co_letter, co_number, ui)
        
        page.run_task(self.update)

    async def update(self):
        while True:

            raw = self.sensors.get_value_array()
            for pos, cell in self.cells.items():
                cell.update(raw[pos])

                
            self.page.update()

            await asyncio.sleep(1/30)
