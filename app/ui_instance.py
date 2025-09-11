
import asyncio
import concurrent.futures
import time
from typing import Callable
import flet as ft

from utilities import color_format
from constants import DEV_LAYOUT
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
    sensor_indicators: dict[tuple[int, int], ft.Container]

    current_player_box: ft.ElevatedButton
    current_player_text: ft.Text

    info_box: ft.Container
    info_text: ft.Text

    ui_enabled: bool = False
    hide_task: concurrent.futures.Future | None = None

    taps: list[float] = []
    tap_exit_time: float = 2
    tap_exit_count: int = 10

    def __init__(self, page: ft.Page):
        self.page = page

        # tabs
        tab_board = UIBuilder.build_tab_board(self)
        tab_sensors = UIBuilder.build_tab_sensors(self)
        self.screens = [tab_board, tab_sensors]

        # content host
        self.content_host = ft.Container(content=tab_board)
        self.info_box = UIBuilder.build_info_box(self)
        self.top_overlay = UIBuilder.build_top_overlay(self)
        self.bottom_overlay = UIBuilder.build_bottom_overlay(self)
        self.root = ft.GestureDetector(
            hover_interval=150,
            on_tap=self.user_activity,
            content=ft.Stack(controls=[self.content_host, self.info_box, self.top_overlay, self.bottom_overlay]),
            height=720,
            width=720,
        )

        if DEV_LAYOUT:
            self.root = ft.Stack(controls=[ft.Row(
                controls=[
                    ft.Container(content=self.screens[0], width=720, height=720),
                    ft.Container(content=self.screens[1], width=720, height=720),
                ],
                spacing=0,
            ), self.info_box])

        page.add(self.root)

    test: float = 0.0

    def update(self):
        self.page.update()

    def update_current_player(self):
        if self.chessboard.get_latest_board() is None or self.chessboard.game_over:
            self.current_player_box.visible = False
        else:
            self.current_player_box.visible = True
            self.current_player_text.value = f"{color_format(self.chessboard.current_player)} plays"

    def on_tab_change(self, e: ft.ControlEvent):
        idx = e.control.selected_index
        self.show_tab(idx)
        self.show_ui()

    def show_tab(self, index: int):
        self.nav.selected_index = index
        self.content_host.content = self.screens[index]

    def board_state_info(self, message: str):
        self.update_board_state(message, color=ft.Colors.WHITE, bgcolor="#54498f")

    def board_state_success(self, message: str):
        self.update_board_state(message, color=ft.Colors.WHITE, bgcolor="#54A800")
        
    def board_state_error(self, message: str):
        self.update_board_state(message, color=ft.Colors.WHITE, bgcolor="#c01010")
        
    def update_board_state(self, message: str, color: str, bgcolor: str):
        self.info_text.value = message
        self.info_text.color = color
        self.info_box.bgcolor = bgcolor
        self.info_box.visible = True

    def hide_board_state(self):
        self.info_box.visible = False

    def notification_info(self, message: str, duration: int | None = None):
        self.send_notification(message, color=ft.Colors.WHITE, bgcolor="#54498f", duration=duration)

    def notification_success(self, message: str, duration: int | None = None):
        self.send_notification(message, color=ft.Colors.WHITE, bgcolor="#54A800", duration=duration)

    def notification_error(self, message: str, duration: int | None = None):
        self.send_notification(message, color=ft.Colors.WHITE, bgcolor="#c01010", duration=duration)

    def send_notification(self, message: str, color: str | None = None, bgcolor: str | None = None, duration: int | None = None):
        text = ft.Text(message, size=24, font_family="Noto Sans Info")
        if color is not None:
            text.color = color

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

        self.exit_sequence()

    def exit_sequence(self):
        now = time.perf_counter()
        self.taps.append(now)

        self.taps = [t for t in self.taps if now - t <= self.tap_exit_time]

        if len(self.taps) > self.tap_exit_count // 2:
            self.notification_info(f"Tap {self.tap_exit_count - len(self.taps)} more times to exit")

        if len(self.taps) >= self.tap_exit_count:
            self.page.window.close()
    
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
            self.hide_task = None

    def sensor_interaction(self, on_click: Callable[[int, int], None]):
        for (co_letter, co_number), el in self.sensor_indicators.items():
            el.on_click = lambda e, x=co_letter, y=co_number: on_click(x, y)