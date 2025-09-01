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

from constants import THEME_WHITE, THEME_BLACK

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
    def build_top_overlay(instance: MagChessUI):

        def get_pgn():
            board = instance.chessboard.get_latest_board()
            if board is None:
                instance.display_message("No game found")
                return None
            else:
                pgn = chess.pgn.Game().from_board(board)
                return str(pgn.mainline())

        def on_pgn_copied(e: ft.ControlEvent):
            pgn = get_pgn()
            if pgn is not None and len(pgn) > 0:
                instance.page.set_clipboard(pgn)
                instance.display_success("PGN copied to clipboard")
            else:
                instance.display_message("Game not found")

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
            filename = f"chess-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.pgn"
            tmp_path = os.path.join(tempfile.gettempdir(), filename)
            with open(tmp_path, "w", encoding="utf-8") as tmp:
                tmp.write(content)

            try:
                cmd = ["gh", "gist", "create", tmp_path]
                return subprocess.run(cmd, check=True)
            except Exception as e:
                instance.display_error("Error creating gist")
            finally:
                os.remove(tmp_path)

        def on_gist_clicked(e: ft.ControlEvent):
            if gh_installed():
                pgn = get_pgn()
                if pgn is not None and len(pgn) > 0:
                    result = create_gist_from_string(pgn)
                    if result is not None:
                        instance.display_success("Gist uploaded successfully")
                else:
                    instance.display_message("Game not found")
            else:
                instance.display_error("GitHub CLI is not installed")

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

        return ft.Stack(
            controls=[copy_pgn_button, gist_button],
            alignment=ft.alignment.top_center,
            animate_offset=150,
            offset=ft.Offset(0, -0.3),
            opacity=0.8,
        )

    @staticmethod
    def build_bottom_overlay(instance: MagChessUI):
        instance.nav = ft.NavigationBar(
            on_change=instance.on_tab_change,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.CROP_FREE, label="Board"),
                ft.NavigationBarDestination(icon=ft.Icons.SENSORS, label="Sensors"),
            ],
        )

        instance.nav_container = ft.Container(
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
            controls=[instance.nav_container],
            alignment=ft.alignment.bottom_center,
            animate_offset=150,
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
                    color= co_number % 2 == 1 and color_light or color_dark,
                    left= 90 * co_number + 66,
                    bottom= -3,
                )
            )

        for co_letter in range(8):
            stack.append(
                ft.Text(
                    chr(ord('A') + co_letter),
                    size=30,
                    font_family="Noto Sans",
                    color= co_letter % 2 == 1 and color_dark or color_light,
                    left= 4,
                    top= 90 * co_letter - 4,
                )
            )

        return stack