import flet as ft

from data import SensorReading
from chessboard import Chessboard
from constants import DEBUG, HW_SENSORS
from ui_instance import MagChessUI
from utilities import asset_path

def main(page: ft.Page):
    page.title = "MagChess"
    page.window.width = 720
    if DEBUG:
        page.window.width = 720 * 3
    page.window.height = 720
    # page.window.full_screen = True
    page.window.frameless = True
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
    
    if HW_SENSORS:
        from sensors_hw import HWSensors
        sensors = HWSensors(on_sensor_reading)
    else:
        from sensors_sw import SWSensors
        sensors = SWSensors(on_sensor_reading)

    # Start
    ui = MagChessUI(page, sensors)
    chessboard = Chessboard(page, ui)

    page.run_task(sensors.sensor_reading_loop)
    page.run_task(chessboard.update)

if __name__ == "__main__":
    ft.app(target=main)
