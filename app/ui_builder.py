from __future__ import annotations
from datetime import datetime
import os
import subprocess
import shutil
import tempfile
import chess
import chess.pgn
import flet as ft
from typing import TYPE_CHECKING

from flet.core.types import MainAxisAlignment

from utilities import sanitize_filename
from constants import THEME_WHITE, THEME_BLACK, PLAYERS_FILE

if TYPE_CHECKING:
    from ui_instance import MagChessUI


class UIBuilder:
    @staticmethod
    def build_tab_board(instance: MagChessUI):
        stack = ft.Stack(
            controls=UIBuilder.build_board(THEME_WHITE, THEME_BLACK),
        )
        instance.board_stack = stack
        return stack

    @staticmethod
    def build_tab_sensors(instance: MagChessUI):
        light = "#999999"
        dark = "#777777"
        stack: list = UIBuilder.build_board(light, dark)

        instance.sensor_indicators = {}
        for co_letter in range(8):
            for co_number in range(8):
                el = ft.Container(
                    width=40,
                    height=40,
                    border=ft.border.all(15, ft.Colors.BLACK),
                    border_radius=ft.border_radius.all(20),
                    left=co_number * 90 + 25,
                    top=co_letter * 90 + 25,
                )
                instance.sensor_indicators[(co_letter, co_number)] = el
                stack.append(el)

        return ft.Stack(
            controls=stack,
        )

    @staticmethod
    def build_info_box(instance: MagChessUI):
        instance.info_text = ft.Text(size=24, color=ft.Colors.WHITE, font_family="Noto Sans Light")
        info_box = ft.Container(
            content=instance.info_text,
            padding=ft.padding.symmetric(14, 24),
            bottom=0,
            left=0,
            right=0,
            height=62,
            visible=False,
        )

        return info_box

    @staticmethod
    def build_tab_players(instance: MagChessUI):
        def save_to_file():
            names = []
            for row in list_view.controls:
                tf = row.controls[0]
                if isinstance(tf, ft.TextField):
                    name = (tf.value or "").strip()
                    if name:
                        names.append(name)
            with open(PLAYERS_FILE, "w", encoding="utf-8") as f:
                f.write("\n".join(names))

        def on_blur(e: ft.ControlEvent):
            save_to_file()
            instance.page.update()

        def on_delete(e: ft.ControlEvent):
            row = e.control.data
            list_view.controls.remove(row)
            save_to_file()
            instance.page.update()

        def on_add(e: ft.ControlEvent):
            name = (new_player.value or "").strip()
            if not name:
                return

            existing = [
                (row.controls[0].value or "").strip().lower()
                for row in list_view.controls
                if isinstance(row.controls[0], ft.TextField)
            ]
            if name.lower() in existing:
                instance.notification_error(f"'{name}' already exists!")
                return

            list_view.controls.append(create_row(name))
            new_player.value = ""
            save_to_file()
            instance.page.update()

        text_field_style = ft.TextStyle(size=24)
        text_file_bg_color = ft.Colors.with_opacity(0.4, ft.Colors.BLACK)
        button_icon_size = 40

        def create_row(text: str):
            row = ft.Row(
                [
                    ft.TextField(
                        value=text,
                        expand=True,
                        bgcolor=text_file_bg_color,
                        on_blur=on_blur,
                        text_style=text_field_style
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="red",
                        on_click=on_delete,
                        data=None,
                        icon_size=button_icon_size
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN
            )

            row.controls[1].data = row
            return row

        if os.path.exists(PLAYERS_FILE):
            with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
                players = [line.strip() for line in f if line.strip()]
        else:
            players = []
        list_view = ft.ListView(expand=True, spacing=10)

        new_player = ft.TextField(
            hint_text="New player name",
            expand=True,
            bgcolor=text_file_bg_color,
            on_blur=on_add,
            text_style=text_field_style,
        )

        new_player_row = ft.Row(
            [
                new_player,
                ft.IconButton(
                    icon=ft.Icons.ADD,
                    icon_color="green",
                    on_click=on_add,
                    icon_size=button_icon_size
                ),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN
        )

        for player in players:
            list_view.controls.append(create_row(player))

        return ft.Stack([
            ft.Container(
                content=ft.Column(
                    [new_player_row, list_view],
                    spacing=10,
                ),
                padding=20,
            )
        ])

    @staticmethod
    def build_top_overlay(instance: MagChessUI):
        def get_pgn():
            board = instance.chessboard.get_latest_board()
            if board is None:
                return None
            else:
                pgn = chess.pgn.Game().from_board(board)
                pgn.headers = instance.chessboard.pgn_headers.to_headers(board.result())
                return str(pgn)

        def on_pgn_copied(e: ft.ControlEvent):
            pgn = get_pgn()
            if pgn is not None and len(pgn) > 0:
                instance.page.set_clipboard(pgn)
                instance.notification_success("PGN copied to clipboard")
            else:
                instance.notification_info("Game not found")

            instance.show_ui()

        copy_pgn_button = ft.ElevatedButton(
            content=ft.Icon(ft.Icons.COPY, size=50),
            on_click=on_pgn_copied,
            top=26,
            left=26,
            color=ft.Colors.WHITE,
            bgcolor="#54A800",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(36, 30),
                shape=ft.RoundedRectangleBorder(20),
            ),
        )

        def gh_installed():
            return shutil.which("gh") is not None

        def create_gist_from_string(content: str):
            filename = sanitize_filename(
                f"chess-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-W_{instance.chessboard.pgn_headers.White}-B_{instance.chessboard.pgn_headers.Black}.pgn")
            tmp_path = os.path.join(tempfile.gettempdir(), filename)
            with open(tmp_path, "w", encoding="utf-8") as tmp:
                tmp.write(content)

            try:
                cmd = ["gh", "gist", "create", tmp_path, "--public"]
                return subprocess.run(cmd, check=True)
            except Exception as e:
                instance.notification_error("Error creating gist")
            finally:
                os.remove(tmp_path)

        def on_gist_clicked(e: ft.ControlEvent):
            if gh_installed():
                pgn = get_pgn()
                if pgn is not None and len(pgn) > 0:
                    result = create_gist_from_string(pgn)
                    if result is not None:
                        instance.notification_success("Gist available at gist.github.com/swift502", duration=10)
                else:
                    instance.notification_info("Game not found")
            else:
                instance.notification_error("GitHub CLI is not installed")

        gist_button = ft.ElevatedButton(
            content=ft.Icon(ft.Icons.UPLOAD, size=50),
            on_click=on_gist_clicked,
            top=26,
            right=26,
            color=ft.Colors.WHITE,
            bgcolor="#8311c0",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(36, 30),
                shape=ft.RoundedRectangleBorder(20),
            ),
        )

        def on_players_clicked(e: ft.ControlEvent):
            players = []
            if os.path.exists(PLAYERS_FILE):
                with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
                    players = [line.strip() for line in f if line.strip()]

            def on_white_changed(e: ft.ControlEvent):
                instance.chessboard.pgn_headers.White = e.control.value

            text_style = ft.TextStyle(size=32)
            option_style = ft.ButtonStyle(text_style=text_style,
                                          shape=ft.RoundedRectangleBorder(0),
                                          padding=ft.padding.symmetric(36, 30))

            white_dd = ft.Dropdown(
                label="White",
                options=[ft.dropdown.Option("White", style=option_style)] +
                        [ft.dropdown.Option(p, style=option_style) for p in players],
                value=instance.chessboard.pgn_headers.White,
                on_change=on_white_changed,
                text_style=text_style,
                label_style=text_style,
                expand=True,
            )

            def on_black_changed(e: ft.ControlEvent):
                instance.chessboard.pgn_headers.Black = e.control.value

            black_dd = ft.Dropdown(
                label="Black",
                options=[ft.dropdown.Option("Black", style=option_style)] +
                        [ft.dropdown.Option(p, style=option_style) for p in players],
                value=instance.chessboard.pgn_headers.Black,
                on_change=on_black_changed,
                text_style=text_style,
                label_style=text_style,
                expand=True,
            )

            def close_dialog(_):
                dialog.open = False
                instance.page.update()

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Select Players"),
                content=ft.Container(
                    content=ft.Column(
                        [white_dd, black_dd],
                        tight=True,
                        spacing=40,
                        width=400,
                    ),
                    margin=ft.margin.only(top=20)
                ),
                actions=[
                    ft.TextButton("Close",
                                  on_click=close_dialog,
                                  style=ft.ButtonStyle(
                                      padding=ft.padding.symmetric(36, 30),
                                      text_style=ft.TextStyle(size=32),
                                  ),
                  )
                ],
                actions_alignment=ft.MainAxisAlignment.END,

            )

            instance.page.open(dialog)

        players_button = ft.ElevatedButton(
            content=ft.Icon(ft.Icons.GROUP, size=50),
            on_click=on_players_clicked,
            top=132 + 10,
            right=26,
            color=ft.Colors.WHITE,
            bgcolor="#ffa500",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(36, 30),
                shape=ft.RoundedRectangleBorder(20),
            ),
        )

        instance.current_player_text = ft.Text(
            "Scanning for\na new game",
            size=30,
            font_family="Noto Sans",
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.WHITE,
        )

        instance.current_player_box = ft.ElevatedButton(
            content=instance.current_player_text,
            top=46,
            bgcolor="#cc1d2024",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(20, 30),
                shape=ft.RoundedRectangleBorder(20),
            ),
            disabled=True,
            visible=False,
        )

        return ft.Stack(
            controls=[copy_pgn_button, gist_button, players_button, instance.current_player_box],
            alignment=ft.alignment.top_center,
            animate_offset=200,
            offset=ft.Offset(0, -0.5),
            opacity=0.8,
        )

    @staticmethod
    def build_bottom_overlay(instance: MagChessUI):
        instance.nav = ft.NavigationBar(
            on_change=instance.on_tab_change,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.CROP_FREE, label="Board"),
                ft.NavigationBarDestination(icon=ft.Icons.SENSORS, label="Sensors"),
                ft.NavigationBarDestination(icon=ft.Icons.GROUP, label="Players"),
            ],
        )

        nav_container = ft.Container(
            content=instance.nav,
            border_radius=ft.border_radius.all(20),
            margin=ft.margin.only(left=16, right=16, bottom=16),
            left=0,
            right=0,
            bottom=0,
            shadow=ft.BoxShadow(
                color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
                blur_radius=8,
                offset=ft.Offset(0, 4),
            ),
        )

        return ft.Stack(
            controls=[nav_container],
            alignment=ft.alignment.bottom_center,
            animate_offset=200,
            offset=ft.Offset(0, 0.2),
            opacity=0.8,
        )

    @staticmethod
    def build_board(color_light: str, color_dark: str):
        rows = []
        for co_letter in range(8):
            row_cells = []
            for co_number in range(8):
                is_dark = (co_letter + co_number) % 2 == 0
                cell = ft.Container(
                    expand=True,
                    bgcolor=color_dark if is_dark else color_light,
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

        stack: list = [board]

        for co_number in range(8):
            stack.append(
                ft.Text(
                    str(co_number + 1),
                    size=30,
                    font_family="Noto Sans",
                    color=co_number % 2 == 1 and color_light or color_dark,
                    left=90 * co_number + 66,
                    bottom=-3,
                )
            )

        for co_letter in range(8):
            stack.append(
                ft.Text(
                    chr(ord('A') + co_letter),
                    size=30,
                    font_family="Noto Sans",
                    color=co_letter % 2 == 1 and color_dark or color_light,
                    left=4,
                    top=90 * co_letter - 4,
                )
            )

        return stack
