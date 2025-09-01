
import asyncio
import concurrent.futures
import math
from typing import Callable
import chess
import flet as ft

from constants import DEV_LAYOUT, RPI
from data import DataLib, IconData, IChessboard
from ui_builder import UIBuilder
from utilities import asset_path, spring

class MagChessUI:
    page: ft.Page
    chessboard: IChessboard

    root: ft.Control
    content_host: ft.Container
    screens: list[ft.Control]
    tab: int
    top_overlay: ft.Stack
    bottom_overlay: ft.Stack
    board_stack: ft.Stack

    nav_container: ft.Container
    nav: ft.NavigationBar

    sensor_indicators: dict[tuple[int, int], ft.Container]

    ui_enabled: bool = False
    auto_hide: bool = True
    hide_task: concurrent.futures.Future | None = None

    advantage: float = 0.5
    adv_value: float = 0.5
    adv_velocity: float = 0.0

    def __init__(self, page: ft.Page, default_tab: int):
        self.page = page

        self.tab = default_tab

        # tabs
        tab2 = UIBuilder.build_tab_2(self)
        tab3 = UIBuilder.build_tab_3(self)
        self.screens = [tab2, tab3]

        # content host
        self.content_host = ft.Container(content=self.screens[default_tab])
        self.top_overlay = UIBuilder.build_top_overlay(self)
        self.bottom_overlay = UIBuilder.build_bottom_overlay(self, default_tab)
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
        self.adv_value, self.adv_velocity = spring(self.adv_value, self.adv_velocity, self.advantage, 10, 0.6)
        assert self.page.window.width

        self.page.update()

    def on_tab_change(self, e: ft.ControlEvent):
        idx = e.control.selected_index
        self.show_tab(idx)
        self.show_ui()

    def show_tab(self, index: int):
        self.tab = index
        self.nav.selected_index = index
        self.content_host.content = self.screens[index]

    def update_move_screen(self, icon: IconData, text: str, player_color: chess.Color | None, rating_screen: bool = False):
        if icon == DataLib.icons.invalid:
            self.display_info(
                text.replace("\n", " "),
                color=ft.Colors.WHITE,
                bgcolor="#54498f",
                )
        elif icon == DataLib.icons.winner:
            self.display_info(
                text.replace("\n", " "),
                color=ft.Colors.BLACK,
                bgcolor="#dbac16",
                duration=10,
            )

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

        if self.auto_hide:
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

    def display_info(self, message: str, color: str | None = None, bgcolor: str | None = None, duration: int | None = None):
        text = ft.Text(message, size=20, font_family="Noto Sans")
        if color is not None:
            text.color = color
        if RPI:
            text.rotate = math.pi

        bar = ft.SnackBar(text)
        if bgcolor is not None:
            bar.bgcolor = bgcolor
        if duration is not None:
            bar.duration = duration * 1000

        if RPI:
            self.page

        self.page.open(bar)

    def display_error(self, message: str):
        self.display_info(message, color=ft.Colors.WHITE, bgcolor="#c01010", duration=10)