from __future__ import annotations
from datetime import datetime
import json
import chess
import chess.pgn
import flet as ft
from typing import TYPE_CHECKING

from constants import THEME_WHITE, THEME_BLACK
from utilities import data_path

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
    def build_top_overlay(instance: MagChessUI):
        def get_pgn():
            board = instance.chessboard.get_latest_board()
            if board is None:
                return None
            else:
                return chess.pgn.Game().from_board(board)

        def upload_highlight(e: ft.ControlEvent):
            pgn = get_pgn()
            if pgn is None:
                instance.notification_info("Game not found")
                return
            else:
                try:
                    with open(data_path("highlights.json"), "r") as f:
                        data: list[object] = json.load(f)
                    data.append({
                        "timestamp": datetime.now().isoformat(timespec='seconds'),
                        "pgn": str(pgn.mainline()),
                    })
                    with open(data_path("highlights.json"), "w") as f:
                        json.dump(data, f, indent=2)

                    instance.notification_success("Highlight uploaded")
                except Exception as ex:
                    print(ex)
                    instance.notification_error(f"Upload failed")
                    return

        upload_highlight_button = ft.ElevatedButton(
            content=ft.Icon(ft.Icons.NOTE_ADD, size=50),
            on_click=upload_highlight,
            top=26,
            left=26,
            color=ft.Colors.WHITE,
            bgcolor="#8311c0",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(36, 30),
                shape=ft.RoundedRectangleBorder(20),
            ),
        )

        def upload_game(e: ft.ControlEvent):
            pgn = get_pgn()
            if pgn is None:
                instance.notification_info("Game not found")
                return
            else:
                try:
                    pgn.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
                    pgn.headers["White"] = "White"
                    pgn.headers["Black"] = "Black"
                    pgn.headers["Result"] = "*"
                    with open(data_path("games.json"), "r") as f:
                        data: list[object] = json.load(f)
                    data.append({
                        "timestamp": datetime.now().isoformat(timespec='seconds'),
                        "white": "White",
                        "black": "Black",
                        "result": "*",
                        "pgn": str(pgn),
                    })
                    with open(data_path("games.json"), "w") as f:
                        json.dump(data, f, indent=2)

                    instance.notification_success("Game uploaded")
                except Exception as ex:
                    print(ex)
                    instance.notification_error(f"Upload failed")
                    return

        upload_game_button = ft.ElevatedButton(
            content=ft.Icon(ft.Icons.SAVE, size=50),
            on_click=upload_game,
            top=26,
            right=26,
            color=ft.Colors.WHITE,
            bgcolor="#0063E4",
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
            controls=[upload_highlight_button, upload_game_button, instance.current_player_box],
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