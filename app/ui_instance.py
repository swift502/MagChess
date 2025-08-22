
import flet as ft
import asyncio
import concurrent.futures

from ui_builder import UIBuilder
from utilities import inverse_lerp, lerp_hex_three
from constants import SENSOR_THRESHOLD_LOW, SENSOR_THRESHOLD_HIGH

class MagChessUI:

    page: ft.Page
    root: ft.Control
    content_host: ft.Container
    overlay: ft.Stack
    replay_button: ft.ElevatedButton
    screens: list[ft.Control]
    _hide_task: concurrent.futures.Future | None = None

    # Colors
    # Green
    col_light = "#eeeed5"
    col_dark = "#7d945d"

    # Brown
    # col_light = "#f0d9b5"
    # col_dark = "#b58863"

    sensor_indicators: dict[tuple[int, int], ft.Container]

    def __init__(self, page: ft.Page, debug: bool):
        self.page = page

        # tabs
        tab1 = UIBuilder.build_tab_1(self)
        tab2 = UIBuilder.build_tab_2(self)
        tab3 = UIBuilder.build_tab_3(self)
        self.screens = [tab1, tab2, tab3]

        if debug:
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
        self.content_host = ft.Container(content=self.screens[1])

        self.overlay = UIBuilder.build_overlay(self)

        self.root = ft.GestureDetector(
            on_hover=self.user_activity,
            hover_interval=150,
            on_tap=self.user_activity,
            on_pan_update=self.user_activity,
            content=ft.Stack(controls=[self.content_host, self.overlay]),
            height=720,
            width=720,
        )

        page.add(self.root)

    def on_tab_change(self, e: ft.ControlEvent):
        idx = e.control.selected_index

        self.content_host.content = self.screens[idx]
        self.replay_button.visible = idx == 1
        
        self.page.update()
        self.user_activity()

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
