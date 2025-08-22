from __future__ import annotations

import flet as ft
from data import DataLib
from pathlib import Path

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui_instance import MagChessUI


class UIBuilder:
    @staticmethod
    def build_tab_1(instance: MagChessUI):
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
        stack: list = UIBuilder.build_board(instance, instance.col_light, instance.col_dark)

        pieces = {
            "a1": DataLib.pieces.white_rook,
            "b1": DataLib.pieces.white_knight,
            "c1": DataLib.pieces.white_bishop,
            "d1": DataLib.pieces.white_queen,
            "e1": DataLib.pieces.white_king,
            "f1": DataLib.pieces.white_bishop,
            "g1": DataLib.pieces.white_knight,
            "h1": DataLib.pieces.white_rook,
            "a2": DataLib.pieces.white_pawn,
            "b2": DataLib.pieces.white_pawn,
            "c2": DataLib.pieces.white_pawn,
            "d2": DataLib.pieces.white_pawn,
            "e2": DataLib.pieces.white_pawn,
            "f2": DataLib.pieces.white_pawn,
            "g2": DataLib.pieces.white_pawn,
            "h2": DataLib.pieces.white_pawn,
            "a8": DataLib.pieces.black_rook,
            "b8": DataLib.pieces.black_knight,
            "c8": DataLib.pieces.black_bishop,
            "d8": DataLib.pieces.black_queen,
            "e8": DataLib.pieces.black_king,
            "f8": DataLib.pieces.black_bishop,
            "g8": DataLib.pieces.black_knight,
            "h8": DataLib.pieces.black_rook,
            "a7": DataLib.pieces.black_pawn,
            "b7": DataLib.pieces.black_pawn,
            "c7": DataLib.pieces.black_pawn,
            "d7": DataLib.pieces.black_pawn,
            "e7": DataLib.pieces.black_pawn,
            "f7": DataLib.pieces.black_pawn,
            "g7": DataLib.pieces.black_pawn,
            "h7": DataLib.pieces.black_pawn,
        }

        for pos, piece in pieces.items():
            row = ord(pos[0]) - ord('a')
            col = int(pos[1]) - 1
            stack.append(ft.Image(
                src=piece.get_path(),
                width=80,
                height=80,
                left=col * 90 + 5,
                top=row * 90 + 5,
            ))

        return ft.Stack(
            controls=stack,
        )

    @staticmethod
    def build_tab_3(instance: MagChessUI):

        light = "#cccccc"
        dark = "#aaaaaa"

        stack: list = UIBuilder.build_board(instance, light, dark)

        instance.sensor_indicators = {}
        for i in range(8):
            for j in range(8):
                el = ft.Container(
                    width=30,
                    height=30,
                    border=ft.border.all(6, ft.Colors.BLACK),
                    border_radius=ft.border_radius.all(15),
                    left=j * 90 + 30,
                    top=i * 90 + 30,
                )
                instance.sensor_indicators[(j, i)] = el
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
    def build_board(instance: MagChessUI, light, dark):
        rows = []
        for r in range(8):
            row_cells = []
            for c in range(8):
                is_dark = (r + c) % 2 == 0
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

        stack: list = [board]

        for i in range(8):
            stack.append(
                ft.Text(
                    str(i + 1),
                    size=30,
                    font_family="Noto Sans",
                    color= i % 2 == 1 and light or dark,
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
                    color= i % 2 == 1 and dark or light,
                    left= 4,
                    top= 90 * i - 4,
                )
            )

        return stack