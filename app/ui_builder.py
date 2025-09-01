from __future__ import annotations
import chess
import chess.pgn
import flet as ft
from typing import TYPE_CHECKING

from constants import THEME_WHITE, THEME_BLACK

if TYPE_CHECKING:
    from ui_instance import MagChessUI

class UIBuilder:
    @staticmethod
    def build_tab_2(instance: MagChessUI):
        stack = ft.Stack(
            controls=UIBuilder.build_board(THEME_WHITE, THEME_BLACK),
        )
        instance.board_stack = stack
        return stack

    @staticmethod
    def build_tab_3(instance: MagChessUI):
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

        def on_pgn_copied(e: ft.ControlEvent):
            board = instance.chessboard.get_latest_board()
            if board is None:
                instance.display_info("No game found")
                return
            
            pgn = chess.pgn.Game().from_board(board)
            instance.page.set_clipboard(str(pgn.mainline()))
            instance.display_info(
                "PGN copied to clipboard",
                color=ft.Colors.WHITE,
                bgcolor="#54A800",
            )

            instance.show_ui()

        instance.copy_pgn_button = ft.ElevatedButton(
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

        return ft.Stack(
            controls=[instance.copy_pgn_button],
            alignment=ft.alignment.top_center,
            animate_offset=150,
            offset=ft.Offset(0, -0.3),
            opacity=0.8,
        )

    @staticmethod
    def build_bottom_overlay(instance: MagChessUI, default_tab: int):
        instance.nav = ft.NavigationBar(
            selected_index=default_tab,
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