import flet as ft

from chessboard import Chessboard
from constants import DEVELOPMENT
from ui_instance import MagChessUI
from utilities import asset_path

def on_key(e: ft.KeyboardEvent, page: ft.Page):
    if e.key == "Escape":
        page.window.close()

def main(page: ft.Page):
    page.title = "MagChess"
    page.window.width = 720
    page.window.height = 720
    if DEVELOPMENT:
        page.window.width = page.window.width * 3
        page.window.frameless = True
    else:
        page.window.full_screen = True
    page.padding = 0
    page.spacing = 0
    page.on_keyboard_event = lambda e: on_key(e, page)
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "Noto Sans": asset_path("fonts/NotoSans-Bold.ttf"),
    }

    # App
    ui = MagChessUI(page)
    chessboard = Chessboard(page, ui)

    # Sensors
    if DEVELOPMENT:
        from sensors_sw import SWSensors
        sensors = SWSensors(chessboard)
        ui.sensor_interaction(sensors.on_sensor_click)
    else:
        from sensors_hw import HWSensors
        sensors = HWSensors(chessboard)

    page.run_task(sensors.sensor_reading_loop)
    page.run_task(chessboard.update)

if __name__ == "__main__":
    ft.app(target=main)
