import flet as ft

from chessboard import Chessboard
from constants import DEV_LAYOUT, RPI
from ui_instance import MagChessUI
from utilities import asset_path

def on_key(e: ft.KeyboardEvent, page: ft.Page):
    if e.key == "Escape":
        page.window.close()
    if e.key == "F11":
        page.window.full_screen = not page.window.full_screen

async def main(page: ft.Page):
    page.title = "MagChess"
    page.window.icon = asset_path("icon.ico")
    page.window.width = 720
    page.window.height = 720
    page.window.frameless = True
    if DEV_LAYOUT:
        page.window.width = page.window.width * 2
    if RPI:
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
    ui.chessboard = chessboard

    if RPI:
        from sensors_hw import HWSensors
        sensors = HWSensors(
            on_sensor_reading=chessboard.update_sensor_value,
            ui=ui,
        )
    else:
        from sensors_sw import SWSensors
        sensors = SWSensors(
            on_sensor_reading=chessboard.update_sensor_value,
            flipped=False,
        )
        ui.sensor_interaction(sensors.on_sensor_click)

    page.run_task(sensors.sensor_reading_loop)
    page.run_task(chessboard.update)

if __name__ == "__main__":
    ft.app(target=main)
