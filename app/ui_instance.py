
import asyncio
import concurrent.futures
from typing import Callable
import chess
import flet as ft

from constants import DEV_LAYOUT
from data import IconData, IChessboard
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
    replay_nav: ft.NavigationBar

    advantage_bar: ft.Container
    copy_pgn_button: ft.ElevatedButton
    replay_button: ft.ElevatedButton

    move_icon: ft.Image
    move_text: ft.Text
    move_background: ft.Container
    sensor_indicators: dict[tuple[int, int], ft.Container]

    _ui_enabled: bool = False
    _hide_task: concurrent.futures.Future | None = None

    _adv_target: float = 0.5
    _adv_value: float = 0.5
    _adv_velocity: float = 0.0

    def __init__(self, page: ft.Page, default_tab: int):
        self.page = page

        # tabs
        tab1 = UIBuilder.build_tab_1(self)
        tab2 = UIBuilder.build_tab_2(self)
        tab3 = UIBuilder.build_tab_3(self)
        self.screens = [tab1, tab2, tab3]

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

        if DEV_LAYOUT:
            self.root = ft.Row(
                controls=[
                    ft.Container(content=self.screens[0], width=720, height=720),
                    ft.Container(content=self.screens[1], width=720, height=720),
                    ft.Container(content=self.screens[2], width=720, height=720),
                ],
                spacing=0,
            )
            
        page.add(self.root)

    def update(self):
        self._adv_value, self._adv_velocity = spring(self._adv_value, self._adv_velocity, self._adv_target, 100, 0.85)
        self.advantage_bar.width = self._adv_value * 720
        self.page.update()

    def on_tab_change(self, e: ft.ControlEvent):
        idx = e.control.selected_index

        self.content_host.content = self.screens[idx]
        
        self.page.update()
        self.show_ui()

    def on_tab_change_replay(self, e: ft.ControlEvent):
        pass

    def update_move_screen(self, icon: IconData, text: str, player_color: chess.Color | None):
        self.move_icon.src = asset_path(icon.image_path)
        self.move_text.value = text
        if player_color is not None:
            self.move_text.value += f"\n{'White' if player_color == chess.WHITE else 'Black'} plays"
        self.move_background.bgcolor = ft.Colors.with_opacity(0.9, icon.color)
        self.page.update()

    def user_activity(self, e: ft.TapEvent | None = None):
        if self._ui_enabled:
            self.hide_ui()
        else:
            self.show_ui()

    def show_ui(self):
        self._ui_enabled = True

        self.top_overlay.offset = ft.Offset(0, 0)
        self.bottom_overlay.offset = ft.Offset(0, 0)
        self.page.update()

        if self._hide_task is not None:
            self._hide_task.cancel()

        self._hide_task = self.page.run_task(self.schedule_hide_ui, 10.0)

    def hide_ui(self):
        self._ui_enabled = False

        self.top_overlay.offset = ft.Offset(0, -0.3)
        self.bottom_overlay.offset = ft.Offset(0, 0.2)
        self.page.update()

        if self._hide_task is not None:
            self._hide_task.cancel()
        
    async def schedule_hide_ui(self, seconds: float):
        try:
            await asyncio.sleep(seconds)
            self.hide_ui()
        except asyncio.CancelledError:
            return

    def sensor_interaction(self, on_click: Callable[[int, int], None]):
        for (co_letter, co_number), el in self.sensor_indicators.items():
            el.on_click = lambda e, x=co_letter, y=co_number: on_click(x, y)

    def set_advantage(self, value: float):
        self._adv_target = value