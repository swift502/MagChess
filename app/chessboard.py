import asyncio
import flet as ft

from cell import Cell
from data import ColorSwap, DataLib, MissingPiece, NewPiece, SensorProvider
from enums import ChessColor
from piece import Piece
from ui_instance import MagChessUI

class Chessboard:
    state_stack: list[dict[tuple[int, int], Piece]]
    staging_state: dict[tuple[int, int], Piece]

    cells: dict[tuple[int, int], Cell]
    spawned_pieces: list[Piece]
    current_player_color: ChessColor

    last_analyzed_sensor_state: str

    def __init__(self, page: ft.Page, ui: MagChessUI, sensors: SensorProvider):
        self.page = page
        self.ui = ui
        self.sensors = sensors
        self.last_analyzed_sensor_state = ""

        self.state_stack = []
        self.staging_state = {}
        self.spawned_pieces = []

        self.cells = {}
        for co_letter in range(8):
            for co_number in range(8):
                self.cells[(co_letter, co_number)] = Cell(co_letter, co_number, ui)
        
        self.pieces = []
        self.current_player_color = ChessColor.WHITE

        page.run_task(self.update)

    async def update(self):
        while True:
            
            # Sensors
            raw = self.sensors.get_value_array()

            # Cells
            for pos, cell in self.cells.items():
                cell.update(raw[pos])

            # Board logic
            if self.match_sensor_state("WW....BB" * 8) and len(self.state_stack) != 1:
                self.init_game()
            else:
                self.update_staging_state()
                
            # Pieces
            for piece in self.pieces:
                piece.update()

            self.page.update()

            await asyncio.sleep(1/30)

    def match_sensor_state(self, state_string: str):
        return self.get_sensor_state_format() == state_string

    def get_sensor_state_format(self):
        string = ""
        for co_letter in range(8):
            for co_number in range(8):
                string += self.cells[(co_letter, co_number)].state_format
        return string

    def init_game(self):
        self.clean_up()

        init_state: dict[tuple[int, int], Piece] = {}

        for locator, pieceData in DataLib.start_configuration().items():
            coords = self.locator_to_coords(locator)
            piece = Piece(self, self.ui, pieceData)
            self.pieces.append(piece)
            init_state[coords] = piece

        self.state_stack.append(init_state)
        self.show_state(init_state)

        print("New game detected")

    def clean_up(self):
        # Pieces
        for piece in self.pieces:
            piece.destroy()
        self.pieces = []

        self.current_player_color = ChessColor.WHITE

        # State
        self.state_stack = []
        self.staging_state = {}

    def locator_to_coords(self, locator: str):
        return (
            ord(locator[0]) - ord("a"),
            int(locator[1]) - 1
        )
    
    def commit_state(self):
        self.state_stack.append(self.staging_state.copy())

    def show_state(self, state: dict[tuple[int, int], Piece]):
        # Iterate state
        for coords, piece in state.items():
            if piece in self.spawned_pieces:
                # Move existing
                piece.go_to(coords)
            else:
                # Spawn new
                piece.spawn(coords)

        # Remove obsolete
        for piece in self.spawned_pieces:
            if piece not in state.values():
                piece.destroy()

    def update_staging_state(self):
        if len(self.state_stack) == 0:
            return

        # Check for changes
        sensor_state = self.get_sensor_state_format()
        if self.last_analyzed_sensor_state == sensor_state:
            return

        # Changes found, start new analysis
        self.last_analyzed_sensor_state = sensor_state
        self.staging_state = self.state_stack[-1].copy()

        new: list[NewPiece] = []
        missing: list[MissingPiece] = []
        swaps: list[ColorSwap] = []

        # Find changes
        for (co_letter, co_number), cell in self.cells.items():
            # Get new color from sensor data
            new_color = cell.color

            # Get old color from last committed state
            piece = self.state_stack[-1].get((co_letter, co_number))

            if piece is None:
                old_color = ChessColor.NONE

                # Found new
                if new_color != ChessColor.NONE:
                    new.append(NewPiece(new_color, (co_letter, co_number)))

            else:
                old_color = piece.color

                # Found missing
                if new_color == ChessColor.NONE:
                    missing.append(MissingPiece(piece, (co_letter, co_number)))

                # Found swap
                elif old_color != new_color:
                    swaps.append(ColorSwap(piece, new_color, (co_letter, co_number)))

        # Results
        missing_new_swaps = (len(missing), len(new), len(swaps))
        print(f"Missing {len(missing)}, New {len(new)}, Swaps {len(swaps)}")

        # Analyze changes
        if missing_new_swaps == (1, 1, 0):

            # Move
            if missing[0].piece.color == new[0].color:
                self.staging_move_piece(missing[0], new[0].coords)

            self.ui.update_move_screen(DataLib.icons.correct, f"Correct")

        elif missing_new_swaps == (1, 0, 1):

            # Capture
            self.staging_remove_piece(swaps[0].coords) # Remove captured piece
            self.staging_move_piece(missing[0], swaps[0].coords) # Move missing piece to capture position

            self.ui.update_move_screen(DataLib.icons.best, f"Best")

        else:
            if self.current_player_color == ChessColor.WHITE:
                self.ui.update_move_screen(DataLib.icons.player_white, "White to move")
            else:
                self.ui.update_move_screen(DataLib.icons.player_black, "Black to move")

        # Finally display the presumed new state
        self.show_state(self.staging_state)

    def staging_move_piece(self, missing: MissingPiece, new_coords: tuple[int, int]):
        self.staging_state[new_coords] = missing.piece
        self.staging_state.pop(missing.coords)

    def staging_remove_piece(self, coords: tuple[int, int]):
        self.staging_state.pop(coords)
