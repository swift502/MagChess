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
                    with open(data_path("highlights.json"), "r", encoding="utf-8") as f:
                        data: list[object] = json.load(f)
                    data.append({
                        "timestamp": datetime.now().isoformat(timespec='seconds'),
                        "pgn": str(pgn.mainline()),
                    })
                    with open(data_path("highlights.json"), "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)

                    instance.notification_success("Highlight uploaded")
                except Exception as ex:
                    print(ex)
                    instance.notification_error(f"Upload failed")
                    return

        upload_highlight_button = ft.ElevatedButton(
            content=ft.Icon(ft.Icons.BOOKMARKS, size=50),
            on_click=upload_highlight,
            top=26,
            left=26,
            color=ft.Colors.WHITE,
            bgcolor="#8710cb",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(36, 30),
                shape=ft.RoundedRectangleBorder(20),
            ),
        )

        def upload_game(white_id: str, black_id: str, players: dict[str, str], result: str):
            pgn = get_pgn()
            if pgn is None:
                instance.notification_info("Game not found")
                return
            else:
                try:
                    pgn.headers.pop("Event")
                    pgn.headers.pop("Site")
                    pgn.headers.pop("Round")
                    pgn.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
                    pgn.headers["White"] = players[white_id]
                    pgn.headers["Black"] = players[black_id]
                    pgn.headers["Result"] = result
                    with open(data_path("games.json"), "r", encoding="utf-8") as f:
                        data: list[object] = json.load(f)
                    data.append({
                        "timestamp": datetime.now().isoformat(timespec='seconds'),
                        "white": white_id,
                        "black": black_id,
                        "result": result,
                        "pgn": str(pgn),
                    })
                    with open(data_path("games.json"), "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)

                    instance.notification_success("Game uploaded")
                except Exception as ex:
                    print(ex)
                    instance.notification_error(f"Upload failed")
                    return

        def upload_game_dialog(e: ft.ControlEvent):
            with open(data_path("players.json"), "r", encoding="utf-8") as f:
                players: dict[str, str] = json.load(f)

            text_style = ft.TextStyle(size=32)
            option_style = ft.ButtonStyle(
                text_style=text_style,
                shape=ft.RoundedRectangleBorder(0),
                padding=ft.padding.symmetric(36, 30),
            )

            select_white = ft.Dropdown(
                label="White",
                options=[ft.dropdown.Option(id, name, style=option_style) for id, name in players.items()],
                # value="0",
                # on_change=on_white_changed,
                text_style=text_style,
                label_style=text_style,
                expand=True,
            )

            select_black = ft.Dropdown(
                label="Black",
                options=[ft.dropdown.Option(id, name, style=option_style) for id, name in players.items()],
                # value="0",
                # on_change=on_black_changed,
                text_style=text_style,
                label_style=text_style,
                expand=True,
            )

            select_result = ft.Dropdown(
                label="Result",
                options=[
                    ft.dropdown.Option("1-0", "White won", style=option_style),
                    ft.dropdown.Option("0-1", "Black won", style=option_style),
                    ft.dropdown.Option("1/2-1/2", "Draw", style=option_style),
                ],
                # value="0",
                # on_change=on_black_changed,
                text_style=text_style,
                label_style=text_style,
                expand=True,
            )

            def commit_game(e: ft.ControlEvent):
                if select_white.value is None or select_black.value is None or select_result.value is None:
                    instance.notification_info("Please select values")
                    return
                
                upload_game(select_white.value, select_black.value, players, select_result.value)
                dialog.open = False
                instance.page.update()

            def close_dialog(e: ft.ControlEvent):
                dialog.open = False
                instance.page.update()

            dialog = ft.AlertDialog(
                modal=True,
                # title=ft.Text("Commit game"),
                # title_text_style=text_style,
                content=ft.Container(
                    content=ft.Column(
                        [select_white, select_black, select_result],
                        tight=True,
                        spacing=40,
                        width=500,
                    ),
                    margin=ft.margin.only(top=20)
                ),
                actions=[
                    ft.TextButton(
                        "Cancel",
                        on_click=close_dialog,
                        style=ft.ButtonStyle(
                            padding=ft.padding.symmetric(36, 30),
                            text_style=text_style,
                            color=ft.Colors.WHITE,
                        ),
                    ),
                    ft.TextButton(
                        "Commit game",
                        on_click=commit_game,
                        style=ft.ButtonStyle(
                            padding=ft.padding.symmetric(32, 36),
                            text_style=text_style,
                            color=ft.Colors.WHITE,
                            bgcolor="#1E8E02",
                        ),
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )

            instance.page.open(dialog)

        upload_game_button = ft.ElevatedButton(
            content=ft.Icon(ft.Icons.SAVE, size=50),
            on_click=upload_game_dialog,
            top=26,
            right=26,
            color=ft.Colors.WHITE,
            bgcolor="#27b200",
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