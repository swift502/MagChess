import flet as ft

page: ft.Page

def tab_1() -> ft.Control:
    img = ft.Image(
        src="https://placehold.co/400x400.png",
    )

    return ft.Container(
        content=ft.Row(
            controls=[ft.Container(content=img, expand=True)],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            # expand=True,
        ),
        # expand=True,
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

    # Center the board
    return ft.Container(
        content=ft.Row(
            [board],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
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


import asyncio
import flet as ft

import asyncio
import flet as ft

def main(ft_page: ft.Page):

    global page
    page = ft_page

    page.title = "MagChess"
    page.window.width = 720
    page.window.height = 720
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    # Your tabs (leave your existing implementations)
    tab1 = tab_1()
    tab2 = tab_2()
    tab3 = tab_3()
    screens = [tab1, tab2, tab3]

    content_host = ft.Container(
        content=screens[0],
        expand=True,
        bgcolor=ft.Colors.ORANGE,
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
            ft.NavigationBarDestination(icon=ft.Icons.CROP_FREE, label="Board"),
            ft.NavigationBarDestination(icon=ft.Icons.TEXT_SNIPPET_OUTLINED, label="Game"),
        ],
    )

    nav_wrap = ft.Container(
        content=nav,
        bgcolor=ft.Colors.with_opacity(0.85, ft.Colors.BLUE),
        border_radius=ft.border_radius.all(20),
        margin=ft.margin.only(left=16, right=16, bottom=16),
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
            expand=True,
            controls=[
                content_host,  # main app content
                nav_wrap,      # overlayed nav (positioned via left/right/bottom)
            ],
        ),
        expand=True,
    )

    page.add(surface)


if __name__ == "__main__":
    ft.app(target=main)
