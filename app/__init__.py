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
    rows = []

    # Green theme
    light = "#7d945d"
    dark = "#eeeed5"

    # Brown theme
    # light = "#f0d9b5"
    # dark = "#b58863"

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

def tab_3():
    chess_games = {
        "2025-08-21 12:13:11": "a",
        "2025-08-21 12:13:12": "b",
        "2025-08-21 12:13:13": "c",
        "2025-08-21 12:13:14": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:15": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:16": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:17": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:18": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:19": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:21": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:22": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:23": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:24": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:25": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:26": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:27": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:28": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:29": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:31": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:32": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:33": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:34": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:35": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:36": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:37": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:38": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:39": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:41": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:42": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:43": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:44": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:45": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:46": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:47": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:48": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:49": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:51": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:52": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:53": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:54": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:55": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:56": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:57": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:58": "1.e4c62.d4d53.Nc3dxe4",
        "2025-08-21 12:13:59": "1.e4c62.d4d53.Nc3dxe4",
    }

    log_view = ft.TextField(
        read_only=True,
        multiline=True,
        min_lines=8,
        border_radius=12,
        text_style=ft.TextStyle(
            font_family="Noto Sans",
            size=24,
        )
    )

    output_snack = ft.SnackBar(content=ft.Text("Copied to clipboard!"), open=False)

    def copy_to_clipboard(e):
        page.set_clipboard(log_view.value or "")
        output_snack.open = True
        page.update()

    copy_btn = ft.FilledButton(
        "Copy",
        icon=ft.Icons.CONTENT_COPY,
        on_click=copy_to_clipboard,
        height=270,
        width=360,
        bgcolor="#7d945d",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(20),
            text_style=ft.TextStyle(
                size=44,
                font_family="Noto Sans",
                color="eeeed5",
            ),
            icon_size=44
            # color="#eeeed5"
            # light = "#7d945d"
            # dark = "#eeeed5"
        ),
    )

    def make_click_handler(ts: str):
        def handler(e):
            log_view.value = chess_games.get(ts, "")
            page.update()
        return handler

    list_items = [
        ft.ListTile(
            title=ft.Text(ts),
            on_click=make_click_handler(ts),
            title_text_style=ft.TextStyle(
                font_family="Noto Sans",
                size=24,
                color="#333333",
            )
        )
        for ts in sorted(chess_games.keys())
    ]

    list_view = ft.ListView(
        controls=list_items,
    )

    if chess_games:
        latest_ts = sorted(chess_games.keys())[0]
        log_view.value = chess_games[latest_ts]

    left_pane = ft.Container(content=list_view, expand=1, padding=10)

    right_pane = ft.Container(
        expand=1,
        padding=10,
        content=ft.Column(
            [
                log_view,
                copy_btn
            ],
        ),
    )

    split = ft.Container(
        content=ft.Row(
            [
                left_pane,
                right_pane
            ],
            height=500
        ),
        height=610,
    )

    # Ensure SnackBar is available on the page
    page.add(output_snack)

    return ft.Container(
        content=split,
        bgcolor="#eeeed5",
        width=720,
        height=720,
        alignment=ft.alignment.top_center,
    )


def main(ft_page: ft.Page):

    global page
    page = ft_page

    page.title = "MagChess"
    page.window.width = 720
    page.window.height = 720
    # page.window.full_screen = True
    # page.window.frameless = True
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {
        "Noto Sans": str(Path(__file__).parent / "assets/fonts/NotoSans-Bold.ttf")
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
        page.update()
        user_activity()

    nav = ft.NavigationBar(
        selected_index=0,
        on_change=on_tab_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.FORK_RIGHT, label="Moves"),
            ft.NavigationBarDestination(icon=ft.Icons.CROP_FREE, label="Board", ),
            ft.NavigationBarDestination(icon=ft.Icons.TEXT_SNIPPET_OUTLINED, label="Logs"),
        ],
    )

    nav_wrap = ft.Container(
        content=nav,
        border_radius=ft.border_radius.all(20),
        margin=ft.margin.only(left=16, right=16, bottom=16),
        animate_opacity=300,
        opacity=0.0,
        left=0, right=0, bottom=0,
        shadow=ft.BoxShadow(
            color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
            blur_radius=8,
            offset=ft.Offset(0, 4)
        )
    )

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
                content_host,
                nav_wrap,
            ],
        ),
        height=720,
        width=720,
    )

    page.add(surface)

if __name__ == "__main__":
    ft.app(target=main)
