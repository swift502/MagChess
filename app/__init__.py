import flet as ft
from pathlib import Path
import asyncio

page: ft.Page

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

    return ft.Container(
        content=ft.Column(
            controls=[img, text],
            alignment=ft.MainAxisAlignment.CENTER,   # vertical centering
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # horizontal centering
        ),
        alignment=ft.alignment.center,  # centers the whole Column in parent
        bgcolor=ft.Colors.with_opacity(0.8, "#96bc4b"),
    )



def tab_2() -> ft.Control:
    rows = []

    # Green theme
    light = "#7d945d"
    dark = "#eeeed5"

    # Brown theme
    # light = "#f0d9b5"
    # dark = "#b58863"

    # 8x8 grid of containers
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
                expand=True,
                aspect_ratio=8.0,
            )
        )

    board = ft.Column(
        controls=rows,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        aspect_ratio=1.0,
    )

    stack = [board]

    for i in range(8):
        stack.append(
            ft.Text(
                i + 1,
                size=30,
                font_family="Noto Sans",
                color= i % 2 == 0 and dark or light,
                left= 90 * i + 58,
                top= 0,  # Below the board
            )
        )

    for i in range(8):
        stack.append(
            ft.Text(
                chr(ord('A') + i),  # Convert 0-7 to A-H
                size=30,
                font_family="Noto Sans",
                color= i % 2 == 0 and dark or light,
                left= 10,  # Left of the board
                top= 90 * i + 40,
            )
        )

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

    # 90x90 squares
    # 60x60 pieces
    # Each piece has 15px margin from the edge of the square
    # Algo is i*90 + 15
    # pawn = ft.Image(
    #     src="",
    #     width=60,
    #     height=60,
    #     left=90 * 4 + 15,  # 4th column (0-indexed)
    #     top= 90 * 4 + 15,  # 4th row (0-indexed)
    # )

    for pos, piece_path in pieces.items():
        row = ord(pos[0]) - ord('a')
        col = int(pos[1]) - 1  # Convert to 0-indexed row
        stack.append(ft.Image(
            src=piece_path,
            width=60,
            height=60,
            left=col * 90 + 15,  # 90px per square, 15px margin
            top=row * 90 + 15,   # 90px per square,
        ))

    # Center the board
    return ft.Container(
        content=ft.Stack(
            controls=stack,
        ),
        expand=True,
    )

def tab_3():

    text_area = ft.TextField(
        label="Write something...",
        hint_text="Type or paste text here",
        multiline=True,
        min_lines=12,
        max_lines=None,
        expand=True,
        border_radius=12,
    )

    output_snack = ft.SnackBar(content=ft.Text("Copied to clipboard!"), open=False)
    page.add(output_snack)

    def copy_to_clipboard(e):
        page.set_clipboard(text_area.value or "")
        output_snack.open = True
        page.update()

    copy_btn = ft.ElevatedButton("Copy", icon=ft.Icons.CONTENT_COPY, on_click=copy_to_clipboard)

    return ft.Container(
        content=ft.Column(
            [
                ft.Row([copy_btn], alignment=ft.MainAxisAlignment.END),
                text_area,
            ],
            expand=True,
        ),
        padding=20,
        expand=True,
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
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {
        "Noto Sans": str(Path(__file__).parent / "assets/fonts/NotoSans-Bold.ttf")
    }

    # page.bgcolor = ft.Colors.with_opacity(0.5, "#96bc4b")
    page.bgcolor = ft.Colors.BLACK

    tab1 = tab_1()
    tab2 = tab_2()
    tab3 = tab_3()
    screens = [tab1, tab2, tab3]

    content_host = ft.Container(
        content=screens[0],
        expand=True,
        alignment=ft.alignment.center,
        # bgcolor=ft.Colors.ORANGE,
    )

    def on_tab_change(e: ft.ControlEvent):
        idx = e.control.selected_index
        content_host.content = screens[idx]
        page.update()
        user_activity()  # keep visible while interacting

    nav = ft.NavigationBar(
        selected_index=0,
        on_change=on_tab_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.FORK_RIGHT, label="Moves"),
            ft.NavigationBarDestination(icon=ft.Icons.CROP_FREE, label="Board", ),
            ft.NavigationBarDestination(icon=ft.Icons.TEXT_SNIPPET_OUTLINED, label="Game"),
        ],
    )

    nav_wrap = ft.Container(
        content=nav,
        # bgcolor=ft.Colors.with_opacity(0.85, ft.Colors.BLUE),
        border_radius=ft.border_radius.all(20),
        margin=ft.margin.only(left=16, right=16, bottom=16),
        # padding=ft.padding.all(8),
        animate_opacity=300,
        opacity=0.0,           # start hidden
        left=0, right=0, bottom=0,  # <-- absolute positioning inside Stack
    )

    # Inactivity timer state
    hide_task: asyncio.Task | None = None

    async def hide_after(seconds: float):
        try:
            await asyncio.sleep(seconds)
            hide_nav()
        except asyncio.CancelledError:
            pass

    def show_nav():
        if not nav_wrap.visible or nav_wrap.opacity < 1:
            nav_wrap.opacity = 1.0
            page.update()

    def hide_nav():
        nav_wrap.opacity = 0.0
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
                content_host,  # main app content
                nav_wrap,      # overlayed nav (positioned via left/right/bottom)
            ],
            alignment=ft.alignment.center,
        ),
        expand=True,
    )

    page.add(surface)

if __name__ == "__main__":
    ft.app(target=main)
