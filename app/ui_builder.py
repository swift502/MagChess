from __future__ import annotations

import chess
import chess.pgn
import flet as ft
from typing import TYPE_CHECKING

from data import DataLib

from constants import THEME_WHITE, THEME_BLACK

if TYPE_CHECKING:
    from ui_instance import MagChessUI

class UIBuilder:
    @staticmethod
    def build_tab_1(instance: MagChessUI):
        instance.move_icon = ft.Image(
            width=320,
            height=320,
        )

        instance.move_text = ft.Text(
            size=72,
            text_align=ft.TextAlign.CENTER,
            font_family="Noto Sans",
            color=ft.Colors.WHITE,
            style=ft.TextStyle(
                shadow=ft.BoxShadow(
                    blur_radius=0,
                    color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                    offset=ft.Offset(0, 8),
                )
            )
        )

        instance.move_background = ft.Container(
            content=ft.Column(
                controls=[instance.move_icon, instance.move_text],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )

        instance.update_move_screen(DataLib.icons.search, "Scanning for\na new game", None)

        return ft.Container(
            content=instance.move_background,
            bgcolor=ft.Colors.BLACK,
        )

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
        instance.advantage_bar = ft.Container(
            bgcolor=ft.Colors.WHITE,
            width=360,
            expand=False
        )

        advantage_display = ft.Container(
            content=ft.Row(controls=[instance.advantage_bar]),
            expand=True,
            bgcolor=ft.Colors.BLACK,
            top=0,
            left=0,
            right=0,
            height=30,
            shadow=ft.BoxShadow(
                color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
                blur_radius=8,
                offset=ft.Offset(0, 4),
            ),
        )

        def on_replay_click(e: ft.ControlEvent):
            states = instance.chessboard.get_latest_state_stack()
            if states is None or len(states) == 0:
                instance.page.open(ft.SnackBar(ft.Text(f"No game found")))
                return
        
            instance.show_tab(1)
            instance.start_game_review(states)

        instance.replay_button = ft.ElevatedButton(
            content=ft.Icon(ft.Icons.HISTORY, size=50),
            on_click=on_replay_click,
            top=54,
            right=26,
            color=ft.Colors.WHITE,
            bgcolor="#8311c0",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(36, 30),
                shape=ft.RoundedRectangleBorder(20),
            ),
        )

        instance.game_review_text = ft.Text(
            "0/0",
            size=30,
            font_family="Noto Sans",
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.WHITE,
        )

        instance.game_review_info = ft.ElevatedButton(
            content=instance.game_review_text,
            top=66,
            bgcolor="#88000000",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(20, 30),
                shape=ft.ContinuousRectangleBorder(20),
            ),
            disabled=True,
            visible=False,
        )

        def on_exit_click(e: ft.ControlEvent):
            instance.exit_game_review()

        instance.exit_button = ft.ElevatedButton(
            content=ft.Icon(ft.Icons.CLOSE, size=50),
            on_click=on_exit_click,
            top=54,
            right=26,
            color=ft.Colors.WHITE,
            bgcolor="#c01010",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(36, 30),
                shape=ft.RoundedRectangleBorder(20),
            ),
            visible=False
        )

        def on_pgn_copied(e: ft.ControlEvent):
            board = instance.chessboard.get_latest_board()
            if board is None:
                instance.page.open(ft.SnackBar(ft.Text(f"No game found")))
                return
            
            pgn = chess.pgn.Game().from_board(board)
            instance.page.set_clipboard(str(pgn.mainline()))
            instance.page.open(ft.SnackBar(ft.Text(f"PGN copied to clipboard")))

            instance.show_ui()

        instance.copy_pgn_button = ft.ElevatedButton(
            content=ft.Icon(ft.Icons.COPY, size=50),
            on_click=on_pgn_copied,
            top=54,
            left=26,
            color=ft.Colors.WHITE,
            bgcolor="#54A800",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(36, 30),
                shape=ft.RoundedRectangleBorder(20),
            ),
        )

        return ft.Stack(
            controls=[advantage_display, instance.replay_button, instance.copy_pgn_button, instance.game_review_info, instance.exit_button],
            alignment=ft.alignment.top_center,
            animate_offset=150,
            offset=ft.Offset(0, -0.3),
        )

    @staticmethod
    def build_bottom_overlay(instance: MagChessUI, default_tab: int):
        instance.nav = ft.NavigationBar(
            selected_index=default_tab,
            on_change=instance.on_tab_change,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.FORK_RIGHT, label="Moves"),
                ft.NavigationBarDestination(icon=ft.Icons.CROP_FREE, label="Board"),
                ft.NavigationBarDestination(icon=ft.Icons.SENSORS, label="Sensors"),
            ],
        )

        instance.replay_nav = ft.NavigationBar(
            selected_index=default_tab,
            on_change=instance.on_tab_change_replay,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.SKIP_PREVIOUS, label="First"),
                ft.NavigationBarDestination(icon=ft.Icons.NAVIGATE_BEFORE, label="Previous"),
                ft.NavigationBarDestination(icon=ft.Icons.NAVIGATE_NEXT, label="Next"),
                ft.NavigationBarDestination(icon=ft.Icons.SKIP_NEXT, label="Last"),
            ],
            overlay_color=ft.Colors.TRANSPARENT,
            indicator_color=ft.Colors.TRANSPARENT,
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