
import asyncio
import concurrent.futures
import math
from typing import Callable
import chess
import flet as ft

from constants import DEV_LAYOUT, RPI
from data import IChessboard
from ui_builder import UIBuilder

class MagChessUI:
    page: ft.Page
    chessboard: IChessboard

    root: ft.Control
    content_host: ft.Container
    screens: list[ft.Control]
    top_overlay: ft.Stack
    bottom_overlay: ft.Stack
    board_stack: ft.Stack
    nav: ft.NavigationBar
    current_player_text: ft.Text
    sensor_indicators: dict[tuple[int, int], ft.Container]

    ui_enabled: bool = False
    hide_task: concurrent.futures.Future | None = None

    def __init__(self, page: ft.Page):
        self.page = page

        # tabs
        tab_board = UIBuilder.build_tab_board(self)
        tab_sensors = UIBuilder.build_tab_sensors(self)
        self.screens = [tab_board, tab_sensors]

        # content host
        self.content_host = ft.Container(content=tab_board)
        self.top_overlay = UIBuilder.build_top_overlay(self)
        self.bottom_overlay = UIBuilder.build_bottom_overlay(self)
        self.root = ft.GestureDetector(
            hover_interval=150,
            on_tap=self.user_activity,
            content=ft.Stack(controls=[self.content_host, self.top_overlay, self.bottom_overlay]),
            height=720,
            width=720,
        )
        if RPI:
            self.root.rotate = math.pi

        if DEV_LAYOUT:
            self.root = ft.Row(
                controls=[
                    ft.Container(content=self.screens[0], width=720, height=720),
                    ft.Container(content=self.screens[1], width=720, height=720),
                ],
                spacing=0,
            )

        page.add(self.root)

    test: float = 0.0

    def update(self):
        self.page.update()

    def update_current_player(self):
        self.current_player_text.value = f"{'White' if self.chessboard.current_player ==  chess.WHITE else 'Black'} plays"

    def on_tab_change(self, e: ft.ControlEvent):
        idx = e.control.selected_index
        self.show_tab(idx)
        self.show_ui()

    def show_tab(self, index: int):
        self.nav.selected_index = index
        self.content_host.content = self.screens[index]

    def display_game(self, message: str):
        self.display_message(message, color=ft.Colors.WHITE, bgcolor="#54498f")

    def display_success(self, message: str):
        self.display_message(message, color=ft.Colors.WHITE, bgcolor="#54A800")
        
    def display_error(self, message: str):
        self.display_message(message, color=ft.Colors.WHITE, bgcolor="#c01010")
        
    def display_message(self, message: str, color: str | None = None, bgcolor: str | None = None, duration: int | None = None):
        text = ft.Text(message, size=24, font_family="Noto Sans")
        if color is not None:
            text.color = color
        if RPI:
            text.rotate = math.pi

        bar = ft.SnackBar(text)
        if bgcolor is not None:
            bar.bgcolor = bgcolor
        if duration is not None:
            bar.duration = duration * 1000

        self.page.open(bar)

    def user_activity(self, e: ft.TapEvent | None = None):
        if self.ui_enabled:
            self.hide_ui()
        else:
            self.show_ui()

    def show_ui(self):
        self.ui_enabled = True

        self.top_overlay.offset = ft.Offset(0, 0)
        self.bottom_overlay.offset = ft.Offset(0, 0)

        self.cancel_hide_task()
        self.hide_task = self.page.run_task(self.schedule_hide_ui, 10.0)

    def hide_ui(self):
        self.ui_enabled = False

        self.top_overlay.offset = ft.Offset(0, -0.3)
        self.bottom_overlay.offset = ft.Offset(0, 0.2)

        self.cancel_hide_task()

    async def schedule_hide_ui(self, seconds: float):
        try:
            await asyncio.sleep(seconds)
            self.hide_ui()
        except asyncio.CancelledError:
            return

    def cancel_hide_task(self):
        if self.hide_task is not None:
            self.hide_task.cancel()

    def sensor_interaction(self, on_click: Callable[[int, int], None]):
        for (co_letter, co_number), el in self.sensor_indicators.items():
            el.on_click = lambda e, x=co_letter, y=co_number: on_click(x, y)