# Chessboard is the game state detector and primary app manager
# Based on sensor values, this class has to infer where all the pieces are, and call ui updates accordingly
# It also communicates with stockfish and hands analysis information over to ui
# Basically it's a three way bridge between sensors, stockfish and the ui

import asyncio
import flet as ft

from sensors import SWSensors
from ui_instance import MagChessUI
from cell import Cell
from piece import Piece

class Chessboard:

    cells: dict[tuple[int, int], Cell]
    pieces: list[Piece]

    # Committed board states
    # Last is current state
    # Game review should use this list
    state_stack: list[dict[tuple[int, int], Piece]]

    @property
    def current_state(self):
        return self.state_stack[-1]

    # Next state
    # Subject to change before commit, can be discarded at any time
    next_state: dict[tuple[int, int], Piece]

    def __init__(self, page: ft.Page, ui: MagChessUI, sensors: SWSensors):
        self.page = page
        self.ui = ui
        self.sensors = sensors

        self.state_stack = []

        self.cells = {}
        for co_letter in range(8):
            for co_number in range(8):
                self.cells[(co_letter, co_number)] = Cell(co_letter, co_number, ui)
        
        self.pieces = []

        page.run_task(self.update)

    async def update(self):
        while True:

            # Sensors
            raw = self.sensors.get_value_array()

            # Cells
            for pos, cell in self.cells.items():
                cell.update(raw[pos])

            # Game start
            if self.match_state(["WW....BB"] * 8) and len(self.state_stack) != 1:
                self.init_game()
                
            self.page.update()

            await asyncio.sleep(1/30)

    def match_state(self, state: list):
        for co_letter in range(8):
            for co_number in range(8):
                cell = self.cells[(co_letter, co_number)].state_format
                check = state[co_letter][co_number]
                if cell == check: continue
                else: return False
        return True

    def init_game(self):
        self.clean_up()
        print("New game detected")

    def clean_up(self):
        # Pieces
        for piece in self.pieces:
            piece.destroy()
        self.pieces = []

        # State
        self.state_stack = []
        self.next_state = {}
