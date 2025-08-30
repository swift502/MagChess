import chess
import chess.engine
from concurrent.futures import Future
import flet as ft

from constants import RPI
from data import IEngine
from utilities import asset_path, inverse_lerp, score_curve
from ui_instance import MagChessUI
    
class Engine(IEngine):
    analyze_task: Future | None = None

    def __init__(self, page: ft.Page, ui: MagChessUI):
        self.page = page
        self.ui = ui

    async def init(self, engine_path: str):
        _, self.engine = await chess.engine.popen_uci(asset_path(engine_path))

    async def analyze(self):
        with await self.engine.analysis(self.board) as analysis:
            async for info in analysis:
                score_data = info.get("score")
                if score_data is not None:
                    if score_data.is_mate():
                        mate = score_data.white().mate()
                        if mate is not None:
                            if abs(mate) < 0.5:
                                score = 0 if score_data.turn else 1
                            else:
                                score = 1 if mate > 0 else 0
                            self.ui.set_advantage(score)
                    else:
                        score = score_data.white().score()
                        if score is not None:
                            normalized = inverse_lerp(-200, 200, float(score))
                            curved = score_curve(normalized)
                            self.ui.set_advantage(curved)
                if info.get("depth", 0) > 20:
                    break

        self.analyze_task = None

    def set_board(self, board: chess.Board):
        self.board = board
        self.cancel_analyze_task()
        self.analyze_task = self.page.run_task(self.analyze)

    def cancel_analyze_task(self):
        if self.analyze_task is not None:
            self.analyze_task.cancel()