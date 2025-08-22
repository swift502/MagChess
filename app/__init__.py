import flet as ft
from pathlib import Path
from ui import MagChessUI

debug = False
debug = True

def main(page: ft.Page):
    page.title = "MagChess"
    page.window.width = 720
    if debug:
        page.window.width = 720 * 3
    page.window.height = 720
    # page.window.full_screen = True
    page.window.frameless = True
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "Noto Sans": str(Path(__file__).parent / "assets/fonts/NotoSans-Bold.ttf"),
    }

    def on_key(e: ft.KeyboardEvent):
        if e.key == "Escape":
            page.window.close()
    page.on_keyboard_event = on_key

    ui = MagChessUI(page, debug)
    page.add(ui.root)

if __name__ == "__main__":
    ft.app(target=main)
