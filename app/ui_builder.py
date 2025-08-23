from __future__ import annotations

import flet as ft
from sensors import SWSensors
from data import DataLib
from pathlib import Path

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui_instance import MagChessUI

import constants as Constants

class UIBuilder:
    @staticmethod
    def build_tab_1():
        img = ft.Image(
            src= str(Path(__file__).parent / "assets/icons/correct.svg"),
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

    @staticmethod
    def build_tab_2(instance: MagChessUI):
        # stack: list = UIBuilder.build_board(Constants.THEME_BRIGHT, Constants.THEME_DARK)

        # for piece in DataLib.get_all_pieces():
        #     el = ft.Image(
        #         src=piece.get_path(),
        #         width=80,
        #         height=80,
        #     )
        #     instance.pieces[pos] = el
        #     stack.append(el)

        stack = ft.Stack(
            controls=UIBuilder.build_board(Constants.THEME_BRIGHT, Constants.THEME_DARK),
        )
        instance.board_stack = stack
        return stack

    @staticmethod
    def build_tab_3(instance: MagChessUI, sensors: SWSensors):

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
                    on_click=lambda e, x=co_letter, y=co_number: sensors.cycle_sensor_state(x, y),
                )
                instance.sensor_indicators[(co_letter, co_number)] = el
                stack.append(el)

        return ft.Stack(
            controls=stack,
        )

    @staticmethod
    def build_overlay(instance: MagChessUI):
        nav = ft.Container(
            content=ft.NavigationBar(
                selected_index=1,
                on_change=instance.on_tab_change,
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.FORK_RIGHT, label="Moves"),
                    ft.NavigationBarDestination(icon=ft.Icons.CROP_FREE, label="Board"),
                    ft.NavigationBarDestination(icon=ft.Icons.SENSORS, label="Sensors"),
                ],
            ),
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

        instance.replay_button = ft.ElevatedButton(
            text=" " + "Review 5 moves",
            on_click=lambda e: print("Replay"),
            top=26,
            bgcolor="#6d10a3",
            color=ft.Colors.WHITE,
            icon=ft.Icons.HISTORY,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=30, font_family="Noto Sans"),
                icon_size=36,
                padding=ft.padding.symmetric(horizontal=34, vertical=26),
                shape=ft.ContinuousRectangleBorder(50),
            ),
        )

        return ft.Stack(
            controls=[nav, instance.replay_button],
            animate_opacity=300,
            opacity=0.0,
            alignment=ft.alignment.center,
        )

    @staticmethod
    def build_board(color_light, color_dark):
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