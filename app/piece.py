from __future__ import annotations

import flet as ft

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chessboard import Chessboard
    from data import PieceData
from ui_instance import MagChessUI
from utilities import asset_path, lerp
    
class Piece:
    def __init__(self, board: Chessboard, ui: MagChessUI, data: PieceData):
        self.board = board
        self.ui = ui
        self.color = data.color
        self.control = ft.Image(
            src=asset_path(data.image_path),
            width=80,
            height=80,
        )

        self.target_cell: tuple[int, int] = (0, 0)

    def update(self):
        target_pos = self.get_top_left(self.target_cell)

        assert self.control.top
        self.control.top = lerp(self.control.top, target_pos[0], 0.3)

        assert self.control.left
        self.control.left = lerp(self.control.left, target_pos[1], 0.3)

    def go_to(self, coords: tuple[int, int]):
        self.target_cell = coords

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