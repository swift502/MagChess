import flet as ft

from data import SensorReading
from chessboard import Chessboard
from constants import DEVELOPMENT
from ui_instance import MagChessUI
from utilities import asset_path

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
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "Noto Sans": asset_path("fonts/NotoSans-Bold.ttf"),
    }

    # Exit event
    def on_key(e: ft.KeyboardEvent):
        if e.key == "Escape":
            page.window.close()
    page.on_keyboard_event = on_key

    # Sensors
    def on_sensor_reading(reading: SensorReading):
        chessboard.update_sensor_values(reading)
    
    if DEVELOPMENT:
        from sensors_sw import SWSensors
        sensors = SWSensors(on_sensor_reading)
    else:
        from sensors_hw import HWSensors
        sensors = HWSensors(on_sensor_reading)

    # Start
    ui = MagChessUI(page, sensors)
    chessboard = Chessboard(page, ui)

    page.run_task(sensors.sensor_reading_loop)
    page.run_task(chessboard.update)

if __name__ == "__main__":
    ft.app(target=main)
