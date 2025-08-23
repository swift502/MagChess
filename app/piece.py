import flet as ft

from utilities import lerp
    
class Piece:
    def __init__(self, control: ft.Image):
        self.control = control

        self.top = 0.0
        self.left = 0.0
        self.target_cell: tuple[int, int] = (0, 0)

    def update(self):
        target_pos = self.get_top_left(self.target_cell)
        self.top = lerp(self.top, target_pos[0], 0.2)
        self.left = lerp(self.left, target_pos[1], 0.2)

        self.control.top = self.top
        self.control.left = self.left

    def go_to(self, co_letter: int, co_number: int):
        self.target_cell = (co_letter, co_number)

    def get_top_left(self, coords: tuple[int, int]):
        return (coords[0] * 90.0 + 5, coords[1] * 90.0 + 5)

    def show(self):
        self.control.visible = True

    def hide(self):
        self.control.visible = False