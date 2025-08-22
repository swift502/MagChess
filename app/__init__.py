import flet as ft
from pathlib import Path
import asyncio

page: ft.Page

def board(light, dark) -> list:

    rows = []

    for r in range(8):
        row_cells = []
        for c in range(8):
            is_dark = (r + c) % 2 == 1
            cell = ft.Container(
                expand=True,
                bgcolor=dark if is_dark else light,
            )
            row_cells.append(cell)
        rows.append(
            ft.Row(
                controls=row_cells,
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                aspect_ratio=8.0,
            )
        )

    board = ft.Column(
        controls=rows,
        spacing=0,
        aspect_ratio=1.0,
    )

    stack = [board]

    for i in range(8):
        stack.append(
            ft.Text(
                i + 1,
                size=30,
                font_family="Noto Sans",
                color= i % 2 == 0 and light or dark,
                left= 90 * i + 66,
                bottom= -3,
            )
        )

    for i in range(8):
        stack.append(
            ft.Text(
                chr(ord('A') + i),
                size=30,
                font_family="Noto Sans",
                color= i % 2 == 0 and dark or light,
                left= 4,
                top= 90 * i - 4,
            )
        )

    return stack

def tab_1() -> ft.Control:
    img = ft.Image(
        src= Path(__file__).parent / "assets/icons/correct.svg",
        width=360,
        height=360,
    )

    text = ft.Text(
        "Correct",
        size=72,
        text_align=ft.TextAlign.CENTER,
        font_family="Noto Sans",
        color=ft.Colors.WHITE,
    )

    foreground = ft.Container(
        content=ft.Column(
            controls=[img, text],
            alignment=ft.MainAxisAlignment.CENTER,   # vertical centering
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # horizontal centering
        ),
        alignment=ft.alignment.center,  # centers the whole Column in parent
        bgcolor=ft.Colors.with_opacity(0.8, "#96bc4b"),
    )

    return ft.Container(
        content=foreground,
        bgcolor=ft.Colors.BLACK,
    )

def tab_2() -> ft.Control:
    # Green theme
    light = "#7d945d"
    dark = "#eeeed5"

    # Brown theme
    # light = "#f0d9b5"
    # dark = "#b58863"

    stack = board(light, dark)

    pieces = {
        "a1": Path(__file__).parent / "assets/pieces/castle_white.svg",
        "b1": Path(__file__).parent / "assets/pieces/knight_white.svg",
        "c1": Path(__file__).parent / "assets/pieces/bishop_white.svg",
        "d1": Path(__file__).parent / "assets/pieces/queen_white.svg",
        "e1": Path(__file__).parent / "assets/pieces/king_white.svg",
        "f1": Path(__file__).parent / "assets/pieces/bishop_white.svg",
        "g1": Path(__file__).parent / "assets/pieces/knight_white.svg",
        "h1": Path(__file__).parent / "assets/pieces/castle_white.svg",
        "a2": Path(__file__).parent / "assets/pieces/pawn_white.svg",
        "b2": Path(__file__).parent / "assets/pieces/pawn_white.svg",
        "c2": Path(__file__).parent / "assets/pieces/pawn_white.svg",
        "d2": Path(__file__).parent / "assets/pieces/pawn_white.svg",
        "e2": Path(__file__).parent / "assets/pieces/pawn_white.svg",
        "f2": Path(__file__).parent / "assets/pieces/pawn_white.svg",
        "g2": Path(__file__).parent / "assets/pieces/pawn_white.svg",
        "h2": Path(__file__).parent / "assets/pieces/pawn_white.svg",
        "a8": Path(__file__).parent / "assets/pieces/castle_black.svg",
        "b8": Path(__file__).parent / "assets/pieces/knight_black.svg",
        "c8": Path(__file__).parent / "assets/pieces/bishop_black.svg",
        "d8": Path(__file__).parent / "assets/pieces/queen_black.svg",
        "e8": Path(__file__).parent / "assets/pieces/king_black.svg",
        "f8": Path(__file__).parent / "assets/pieces/bishop_black.svg",
        "g8": Path(__file__).parent / "assets/pieces/knight_black.svg",
        "h8": Path(__file__).parent / "assets/pieces/castle_black.svg",
        "a7": Path(__file__).parent / "assets/pieces/pawn_black.svg",
        "b7": Path(__file__).parent / "assets/pieces/pawn_black.svg",
        "c7": Path(__file__).parent / "assets/pieces/pawn_black.svg",
        "d7": Path(__file__).parent / "assets/pieces/pawn_black.svg",
        "e7": Path(__file__).parent / "assets/pieces/pawn_black.svg",
        "f7": Path(__file__).parent / "assets/pieces/pawn_black.svg",
        "g7": Path(__file__).parent / "assets/pieces/pawn_black.svg",
        "h7": Path(__file__).parent / "assets/pieces/pawn_black.svg",
    }

    for pos, piece_path in pieces.items():
        row = ord(pos[0]) - ord('a')
        col = int(pos[1]) - 1
        stack.append(ft.Image(
            src=piece_path,
            width=80,
            height=80,
            left=col * 90 + 5,
            top=row * 90 + 5,
        ))

    return ft.Stack(
        controls=stack,
    )

def tab_3() -> ft.Container:

    light = "#cccccc"
    dark = "#aaaaaa"

    sensor_positive = "#0000ff"
    sensor_negative = "#ff0000"
    sensor_neutral = "#000000"

    stack = board(light, dark)

    for i in range(8):
        for j in range(8):
            stack.append(ft.Container(
                bgcolor=(i + j) % 2 == 1 and sensor_positive or sensor_negative,
                width=20,
                height=20,
                border_radius=10,
                left=j * 90 + 35,
                top=i * 90 + 35,
            ))

    return ft.Stack(
        controls=stack,
    )

def main(ft_page: ft.Page):

    global page
    page = ft_page

    page.title = "MagChess"
    page.window.width = 720
    page.window.height = 720
    # page.window.full_screen = True
    page.window.frameless = True
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "Noto Sans": str(Path(__file__).parent / "assets/fonts/NotoSans-Bold.ttf"),
        "Noto Sans Light": str(Path(__file__).parent / "assets/fonts/NotoSans-Regular.ttf")
    }

    page.bgcolor = ft.Colors.RED

    tab1 = tab_1()
    tab2 = tab_2()
    tab3 = tab_3()
    screens = [tab1, tab2, tab3]

    content_host = ft.Container(
        content=screens[1],
    )

    def on_tab_change(e: ft.ControlEvent):
        idx = e.control.selected_index
        content_host.content = screens[idx]
        replay_button.visible = (idx == 1)
        page.update()
        user_activity()

    nav = ft.Container(
        content=ft.NavigationBar(
            selected_index=1,
            on_change=on_tab_change,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.FORK_RIGHT, label="Moves"),
                ft.NavigationBarDestination(icon=ft.Icons.CROP_FREE, label="Board"),
                ft.NavigationBarDestination(icon=ft.Icons.SENSORS, label="Sensors"),
            ],
        ),
        border_radius=ft.border_radius.all(20),
        margin=ft.margin.only(left=16, right=16, bottom=16),
        # animate_opacity=300,
        # opacity=0.0,
        left=0, right=0, bottom=0,
        shadow=ft.BoxShadow(
            color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
            blur_radius=8,
            offset=ft.Offset(0, 4)
        )
    )

    replay_button = ft.ElevatedButton(
        text=" Review game",
        on_click=lambda e: print("Replay"),
        top=26,
        left=22,
        bgcolor="#6d10a3",
        color=ft.Colors.WHITE,
        icon=ft.Icons.HISTORY,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(
                size=32,
                font_family="Noto Sans"
            ),
            icon_size=36,
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
        ),
    )

    overlay = ft.Stack(
        controls=[
            nav,
            replay_button,
        ],
        animate_opacity=300,
        opacity=0.0,
    )

    hide_task: asyncio.Task | None = None

    async def hide_after(seconds: float):
        try:
            await asyncio.sleep(seconds)
            hide_nav()
        except asyncio.CancelledError:
            pass

    def show_nav():
        overlay.opacity = 1.0
        page.update()

    def hide_nav():
        overlay.opacity = 0.0
        page.update()

    def schedule_hide():
        nonlocal hide_task
        if hide_task is not None:
            hide_task.cancel()
        hide_task = page.run_task(hide_after, 1.0)

    def user_activity(_=None):
        show_nav()
        schedule_hide()

    surface = ft.GestureDetector(
        on_hover=user_activity,
        hover_interval=150,
        on_tap=user_activity,
        on_pan_update=user_activity,
        content=ft.Stack(
            controls=[
                content_host,
                overlay,
            ],
        ),
        height=720,
        width=720,
    )

    page.add(surface)

if __name__ == "__main__":
    ft.app(target=main)
