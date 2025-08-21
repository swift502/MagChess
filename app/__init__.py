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
            expand=True,
        ),
        expand=True,
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


def main(ft_page: ft.Page):

    global page
    page = ft_page

    page.title = "Three-tab Flet Demo"
    # page.window.full_screen = True  # fullscreen for desktop
    page.window.width = 720
    page.window.height = 720
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    tab1 = tab_1()
    tab2 = tab_2()
    tab3 = tab_3()

    screens = [tab1, tab2, tab3]
    content_host = ft.Container(content=screens[0], expand=True)

    def on_tab_change(e: ft.ControlEvent):
        idx = e.control.selected_index
        content_host.content = screens[idx]
        page.update()

    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_tab_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.IMAGE, label="Image"),
            ft.NavigationBarDestination(icon=ft.Icons.GRID_ON, label="Chess"),
            ft.NavigationBarDestination(icon=ft.Icons.TEXT_SNIPPET, label="Text"),
        ],
    )

    # Root layout: content + nav bar pinned at bottom
    page.add(
        ft.Column(
            [
                ft.Container(content=content_host, expand=True),
            ],
            expand=True,
            spacing=0,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
