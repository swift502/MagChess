from __future__ import annotations

import flet as ft

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chessboard import Chessboard
from ui_instance import MagChessUI
from utilities import lerp
    
class Piece:
    def __init__(self, board: Chessboard, ui: MagChessUI, control: ft.Image):
        self.board = board
        self.ui = ui
        self.control = control

        self.target_cell: tuple[int, int] = (0, 0)

        ui.board_stack.controls.append(control)

    def update(self):
        target_pos = self.get_top_left(self.target_cell)

        assert self.control.top
        self.control.top = lerp(self.control.top, target_pos[0], 0.2)

        assert self.control.left
        self.control.left = lerp(self.control.left, target_pos[1], 0.2)

    def go_to(self, co_letter: int, co_number: int):
        self.target_cell = (co_letter, co_number)

    def get_top_left(self, coords: tuple[int, int]):
        return (coords[0] * 90.0 + 5, coords[1] * 90.0 + 5)

    def spawn(self, coords):
        self.ui.board_stack.controls.append(self.control)
        self.target_cell = coords
        self.control.top, self.control.left = self.get_top_left(coords)

        self.board.spawned_pieces.append(self)

    def destroy(self):
        self.ui.board_stack.controls.remove(self.control)
        self.board.spawned_pieces.remove(self)