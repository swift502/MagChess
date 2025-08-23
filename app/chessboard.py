# Chessboard is the game state detector and primary app manager
# Based on sensor values, this class has to infer where all the pieces are, and call ui updates accordingly
# It also communicates with stockfish and hands analysis information over to ui
# Basically it's a three way bridge between sensors, stockfish and the ui

import asyncio
import flet as ft

from data import DataLib
from sensors import SWSensors
from ui_instance import MagChessUI
from cell import Cell
from piece import Piece

class Chessboard:

    cells: dict[tuple[int, int], Cell]
    spawned_pieces: list[Piece]

    # Committed board states
    # Last is current state
    # Game review should use this list
    state_stack: list[dict[tuple[int, int], Piece]]

    @property
    def current_state(self):
        return self.state_stack[-1]

    # Next state
    # Subject to change before commit, can be discarded at any time
    staging_state: dict[tuple[int, int], Piece]

    def __init__(self, page: ft.Page, ui: MagChessUI, sensors: SWSensors):
        self.page = page
        self.ui = ui
        self.sensors = sensors

        self.state_stack = []
        self.staging_state = {}
        self.spawned_pieces = []

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
                
            # Pieces
            for piece in self.pieces:
                piece.update()

            self.page.update()

            await asyncio.sleep(1/30)

    def match_state(self, state: list):
        for co_letter in range(8):
            for co_number in range(8):
                actual = self.cells[(co_letter, co_number)].state_format
                desired = state[co_letter][co_number]
                if actual == desired: continue
                else: return False
        return True

    def init_game(self):
        self.clean_up()

        for locator, piece in DataLib.start_configuration().items():
            coords = self.locator_to_coords(locator)
            image = ft.Image(
                src=piece.get_path(),
                width=80,
                height=80,
            )
            piece = Piece(self, self.ui, image)
            self.pieces.append(piece)
            self.staging_state[coords] = piece

        self.commit_state()
        self.show_state(self.staging_state)

        print("New game detected")

    def clean_up(self):
        # Pieces
        for piece in self.pieces:
            piece.destroy()
        self.pieces = []

        # State
        self.state_stack = []
        self.staging_state = {}

    def locator_to_coords(self, locator: str):
        return (
            ord(locator[0]) - ord("a"),
            int(locator[1]) - 1
        )
    
    def commit_state(self):
        self.state_stack.append(self.staging_state)

    def show_state(self, state: dict[tuple[int, int], Piece]):
        # Iterate state
        for coords, piece in state.items():
            if piece in self.spawned_pieces:
                # Move existing
                piece.go_to(coords[0], coords[1])
            else:
                # Spawn new
                piece.spawn(coords)

        # Remove obsolete
        for piece in self.spawned_pieces:
            if piece not in state.values():
                piece.destroy()
