
import asyncio
import concurrent.futures
import math
from typing import Callable
import chess
import flet as ft

from constants import DEV_LAYOUT, RPI
from data import BoardState, DataLib, IEngine, IconData, IChessboard
from ui_builder import UIBuilder
from utilities import asset_path, spring

class MagChessUI:
    page: ft.Page
    chessboard: IChessboard
    engine: IEngine

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

    advantage_display: ft.Container
    advantage_bar: ft.Container
    copy_pgn_button: ft.ElevatedButton
    game_review_info: ft.ElevatedButton
    game_review_text: ft.Text
    replay_button: ft.ElevatedButton
    exit_button: ft.ElevatedButton

    move_icon: ft.Image
    move_text: ft.Text
    move_background: ft.Container
    sensor_indicators: dict[tuple[int, int], ft.Container]

    game_review: bool = False
    game_review_states: list[BoardState] | None = None
    game_review_index: int = 0

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
        if RPI:
            self.root.rotate = math.pi

        if DEV_LAYOUT:
            self.root = ft.Stack(controls=[ft.Row(
                controls=[
                    ft.Container(content=self.screens[0], width=720, height=720),
                    ft.Container(content=self.screens[1], width=720, height=720),
                    ft.Container(content=self.screens[2], width=720, height=720),
                ],
                spacing=0,
            ), self.advantage_display])
            
        page.add(self.root)

    test: float = 0.0

    def update(self):
        self.adv_value, self.adv_velocity = spring(self.adv_value, self.adv_velocity, self.advantage, 10, 0.6)
        assert self.page.window.width
        self.advantage_bar.width = self.adv_value * self.page.window.width

        if self.move_rating_screen:
            states = self.chessboard.get_latest_state_stack()
            if states is not None and len(states) > 0:
                delta = self.adv_value - states[-1].advantage
                if self.chessboard.current_player == chess.BLACK:
                    delta = -delta
                rating_icon, rating_text = self.get_move_rating(delta)
                self.update_move_screen(rating_icon, rating_text, self.chessboard.next_player, rating_screen=True)

        self.page.update()

    def get_move_rating(self, delta: float):
        if delta > 0.15:
            return DataLib.icons.brilliant, "Brilliant!"
        elif delta > 0.1:
            return DataLib.icons.great_find, "Great find!"
        elif delta > 0.05:
            return DataLib.icons.excellent, "Excellent!"
        elif delta > 0.0:
            return DataLib.icons.correct, "Correct"
        elif delta > -0.1:
            return DataLib.icons.good, "Good"
        elif delta > -0.2:
            return DataLib.icons.inaccuracy, "Risky"
        elif delta > -0.3:
            return DataLib.icons.incorrect, "Bad move!"
        elif delta > -0.4:
            return DataLib.icons.mistake, "Mistake!"
        else:
            return DataLib.icons.blunder, "Blunder!"

    def on_tab_change(self, e: ft.ControlEvent):
        idx = e.control.selected_index
        self.show_tab(idx)
        self.show_ui()

    def show_tab(self, index: int):
        self.tab = index
        self.nav.selected_index = index
        self.content_host.content = self.screens[index]
        self.page.update()

    def on_tab_change_replay(self, e: ft.ControlEvent):
        idx = e.control.selected_index

        if idx == 0:
            self.review_first()
        elif idx == 1:
            self.review_previous()
        elif idx == 2:
            self.review_next()
        elif idx == 3:
            self.review_last()

    def update_move_screen(self, icon: IconData, text: str, player_color: chess.Color | None, rating_screen: bool = False):
        self.move_icon.src = asset_path(icon.image_path)
        self.move_text.value = text
        if player_color is not None:
            self.move_text.value += f"\n{'White' if player_color == chess.WHITE else 'Black'} plays"
        self.move_background.bgcolor = ft.Colors.with_opacity(0.9, icon.color)

        if not rating_screen:
            self.move_rating_screen = False

        if self.tab in (1, 2):
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

        self.page.update()

    def user_activity(self, e: ft.TapEvent | None = None):
        if self.ui_enabled:
            self.hide_ui()
        else:
            self.show_ui()

    def show_ui(self):
        self.ui_enabled = True

        self.top_overlay.offset = ft.Offset(0, 0)
        self.bottom_overlay.offset = ft.Offset(0, 0)
        self.page.update()

        self.cancel_hide_task()

        if self.auto_hide:
            self.hide_task = self.page.run_task(self.schedule_hide_ui, 10.0)

    def hide_ui(self):
        self.ui_enabled = False

        self.top_overlay.offset = ft.Offset(0, -0.3)
        self.bottom_overlay.offset = ft.Offset(0, 0.2)
        self.page.update()

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

    def set_advantage(self, value: float):
        self.advantage = value
    
    def start_game_review(self, states: list[BoardState]):
        if self.game_review:
            return

        self.copy_pgn_button.visible = False
        self.replay_button.visible = False
        self.exit_button.visible = True
        self.game_review_info.visible = True

        self.cancel_hide_task()
        self.auto_hide = False
        self.show_ui()
        self.nav_container.content = self.replay_nav

        self.game_review = True
        self.game_review_states = states
        self.game_review_index = len(states) - 1

        self.engine.cancel_analyze_task()
        self.show_review_state()

    def exit_game_review(self):
        if not self.game_review:
            return

        self.copy_pgn_button.visible = True
        self.replay_button.visible = True
        self.exit_button.visible = False
        self.game_review_info.visible = False

        self.nav_container.content = self.nav
        self.auto_hide = True
        self.show_ui()

        self.game_review = False
        self.game_review_states = None
        self.game_review_index = 0

        self.chessboard.show_state(self.chessboard.staging_state)

        states = self.chessboard.get_latest_state_stack()
        if states is not None and len(states) > 1:
            latest_board = self.chessboard.get_latest_board()
            if latest_board is not None:
                self.engine.set_board(latest_board)

    def show_review_state(self):
        if self.game_review_states is None:
            return
        
        self.game_review_text.value = f"{self.game_review_index + 1}/{len(self.game_review_states)}"
        state = self.game_review_states[self.game_review_index]
        self.chessboard.show_state(state)
        self.set_advantage(state.advantage)

    def clamp_review_index(self):
        if self.game_review_states is None:
            return

        if self.game_review_index < 0:
            self.game_review_index = 0
        elif self.game_review_index > len(self.game_review_states) - 1:
            self.game_review_index = len(self.game_review_states) - 1

    def review_next(self):
        self.game_review_index += 1
        self.clamp_review_index()
        self.show_review_state()

    def review_previous(self):
        self.game_review_index -= 1
        self.clamp_review_index()
        self.show_review_state()

    def review_first(self):
        self.game_review_index = 0
        self.show_review_state()

    def review_last(self):
        if self.game_review_states is None:
            return
        
        self.game_review_index = len(self.game_review_states) - 1
        self.show_review_state()

    def display_info(self, message: str, color: str | None = None, bgcolor: str | None = None, duration: int | None = None):
        text = ft.Text(message, size=20, font_family="Noto Sans")
        if color is not None:
            text.color = color

        bar = ft.SnackBar(text)
        if bgcolor is not None:
            bar.bgcolor = bgcolor
        if duration is not None:
            bar.duration = duration * 1000

        self.page.open(bar)

    def display_error(self, message: str):
        self.display_info(message, color=ft.Colors.WHITE, bgcolor="#c01010", duration=10)