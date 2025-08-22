# Chessboard is the game state manager
# Based on sensor values, this class has to infer where all the pieces are, and call ui updates accordingly
# It also communicates with stockfish and hands analysis information to ui
# Basically it's a three way bridge between sensors, stockfish and the ui

import asyncio
import flet as ft

class Chessboard:
    def __init__(self, page: ft.Page):
        page.run_task(self.update)

    async def update(self):
        while True:

            print("Update")

            await asyncio.sleep(1/60)
