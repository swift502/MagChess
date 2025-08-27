
import asyncio
import concurrent.futures
from typing import Callable
import chess
import flet as ft

from constants import DEV_LAYOUT
from data import IconData, IChessboard
from ui_builder import UIBuilder
from utilities import asset_path

class MagChessUI:
    page: ft.Page
    chessboard: IChessboard

    root: ft.Control
    content_host: ft.Container
    screens: list[ft.Control]
    overlay: ft.Stack

    copy_pgn_button: ft.ElevatedButton
    replay_button: ft.ElevatedButton

    board_stack: ft.Stack
    pieces: dict[tuple[int, int], ft.Image]
    sensor_indicators: dict[tuple[int, int], ft.Container]
    _hide_task: concurrent.futures.Future | None = None

    move_icon: ft.Image
    move_text: ft.Text
    move_background: ft.Container

    def __init__(self, page: ft.Page, default_tab: int):
        self.page = page

        # tabs
        tab1 = UIBuilder.build_tab_1(self)
        tab2 = UIBuilder.build_tab_2(self)
        tab3 = UIBuilder.build_tab_3(self)
        self.screens = [tab1, tab2, tab3]

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
            return

        # content host
        self.content_host = ft.Container(content=self.screens[default_tab])
        self.overlay = UIBuilder.build_overlay(self, default_tab)
        self.root = ft.GestureDetector(
            on_hover=self.user_activity,
            hover_interval=150,
            on_tap=self.user_activity,
            on_pan_update=self.user_activity,
            content=ft.Stack(controls=[self.content_host, self.overlay]),
            height=720,
            width=720,
        )

        self.refresh_tab_ui(default_tab)
        page.add(self.root)

    def on_tab_change(self, e: ft.ControlEvent):
        idx = e.control.selected_index

        self.content_host.content = self.screens[idx]
        self.refresh_tab_ui(idx)
        
        self.page.update()
        self.user_activity()

    def refresh_tab_ui(self, tab: int):
        self.copy_pgn_button.visible = tab == 0
        self.replay_button.visible = tab == 1

    def update_move_screen(self, icon: IconData, text: str, player_color: chess.Color | None):
        self.move_icon.src = asset_path(icon.image_path)
        self.move_text.value = text
        if player_color is not None:
            self.move_text.value += f"\n{"White" if player_color == chess.WHITE else "Black"} plays"
        self.move_background.bgcolor = ft.Colors.with_opacity(0.9, icon.color)
        self.page.update()

    async def hide_after(self, seconds: float):
        try:
            # Wait
            await asyncio.sleep(seconds)

            # Hide
            self.overlay.opacity = 0.0
            self.page.update()
        except asyncio.CancelledError:
            pass

    def user_activity(self, _=None):
        # Show
        self.overlay.opacity = 1.0
        self.page.update()
        
        # Schedule hide
        if self._hide_task is not None:
            self._hide_task.cancel()
        self._hide_task = self.page.run_task(self.hide_after, 1.0)

    def sensor_interaction(self, on_click: Callable[[int, int], None]):
        for (co_letter, co_number), el in self.sensor_indicators.items():
            el.on_click = lambda e, x=co_letter, y=co_number: on_click(x, y)