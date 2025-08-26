from __future__ import annotations
import asyncio
import typing
import flet as ft

from cell import Cell
import chess
from data import ColorSwap, DataLib, MissingPiece, NewPiece, SensorProvider
from piece import Piece
from ui_instance import MagChessUI

if typing.TYPE_CHECKING:
    from typing_extensions import TypeAlias

BoardState: TypeAlias = dict[tuple[int, int], Piece]

class Chessboard:
    board: chess.Board
    state_stack: list[BoardState]
    staging_state: BoardState

    cells: dict[tuple[int, int], Cell]
    spawned_pieces: list[Piece]
    current_player: chess.Color

    last_analysed_sensor_state: str | None
    last_legal_move: chess.Move | None

    @property
    def next_player(self):
        return chess.WHITE if self.current_player == chess.BLACK else chess.BLACK

    def __init__(self, page: ft.Page, ui: MagChessUI, sensors: SensorProvider):
        self.page = page
        self.ui = ui
        self.sensors = sensors
        
        self.state_stack = []
        self.staging_state = {}
        self.spawned_pieces = []
        self.game_over: bool = False

        self.cells = {}
        for co_letter in range(8):
            for co_number in range(8):
                self.cells[(co_letter, co_number)] = Cell(co_letter, co_number, ui)
        
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
            elif not self.game_over:
                self.board_state_update()
                
            # Pieces
            for piece in self.spawned_pieces:
                piece.update()

            # Update
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

        self.board = chess.Board()

        init_state: BoardState = {}
        self.last_analysed_sensor_state = None
        self.last_legal_move = None

        for locator, pieceData in DataLib.start_configuration().items():
            coords = self.locator_to_coords(locator)
            piece = Piece(self, self.ui, pieceData)
            init_state[coords] = piece

        self.state_stack.append(init_state)
        self.show_state(init_state)

        print("New game detected")

    def clean_up(self):
        self.game_over = False
        self.current_player = chess.WHITE

        # State
        self.state_stack = []
        self.staging_state = {}

        # Clean up entities
        self.show_state(self.staging_state)

    def locator_to_coords(self, locator: str):
        return (
            ord(locator[0]) - ord("a"),
            int(locator[1]) - 1
        )

    def coords_to_locator(self, coords: tuple[int, int]):
        return chr(coords[0] + ord("a")) + str(coords[1] + 1)
    
    def commit_staging_state(self, move: chess.Move):
        self.state_stack.append(self.staging_state.copy())
        self.board.push(move)
        self.current_player = self.next_player
        print(f"Committed {move.uci()}")

    def show_state(self, state: BoardState):
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

    def board_state_update(self):
        if len(self.state_stack) == 0:
            return

        # Check for changes
        sensor_state = self.get_sensor_state_format()
        if self.last_analysed_sensor_state == sensor_state:
            return

        # Changes found, start new analysis
        self.last_analysed_sensor_state = sensor_state

        # See if conditions are met to commit the last staging state
        self.state_commit_processing()

        # Staging state may have been committed now, we can safely discard it
        self.staging_state = self.state_stack[-1].copy()
        self.last_legal_move = None

        # Analyse changes against latest committed state
        missing, new, swaps = self.analyse_sensor_changes(against=self.state_stack[-1])
        print(f"Missing {len(missing)}, New {len(new)}, Swaps {len(swaps)}")

        # Update staging state
        move = self.update_staging_state(missing, new, swaps)
        self.show_state(self.staging_state)

        if move is not None:
            move = chess.Move.from_uci(move)

            if move in self.board.legal_moves:
                self.last_legal_move = move

                outcome_board = self.board.copy()
                outcome_board.push(move)
                outcome = outcome_board.outcome()
                if outcome is None:
                    self.ui.update_move_screen(DataLib.icons.good, f"Legal move")
                else:
                    self.game_over = True
                    self.ui.update_move_screen(DataLib.icons.winner, f"Game over!\nWinner: {self.get_winner_string(outcome.winner)}")
            else:
                self.ui.update_move_screen(DataLib.icons.invalid, f"Illegal move")

    def state_commit_processing(self):
        if self.last_legal_move is None:
            return

        # If last analysis concluded a legal move, and now we find
        # the other player is moving pieces, we need to commit
        missing, new, swaps = self.analyse_sensor_changes(against=self.staging_state)

        for piece in missing:
            if piece.piece.color == self.next_player:
                self.commit_staging_state(self.last_legal_move)
                return

        for piece in new:
            if piece.color == self.next_player:
                self.commit_staging_state(self.last_legal_move)
                return

        if len(swaps) > 0:
            self.commit_staging_state(self.last_legal_move)
            return

    def analyse_sensor_changes(self, against: BoardState):
        missing: list[MissingPiece] = []
        new: list[NewPiece] = []
        swaps: list[ColorSwap] = []

        # Find changes
        for coords, cell in self.cells.items():
            # Get new color from sensor data
            new_color = cell.color

            # Get old color from last committed state
            piece = against.get(coords)

            if piece is None:
                old_color = None

                # Found new
                if new_color != None:
                    new.append(NewPiece(new_color, coords))

            else:
                old_color = piece.color

                # Found missing
                if new_color == None:
                    missing.append(MissingPiece(piece, coords))

                # Found swap
                elif old_color != new_color:
                    swaps.append(ColorSwap(piece, new_color, coords))

        return missing, new, swaps

    def update_staging_state(self, missing : list[MissingPiece], new: list[NewPiece], swaps: list[ColorSwap]) -> str | None:
        missing_new_swaps = (len(missing), len(new), len(swaps))

        if missing_new_swaps == (1, 1, 0):
            move = chess.Move.from_uci(self.coords_to_locator(missing[0].coords) + self.coords_to_locator(new[0].coords))
            if missing[0].piece.pieceType == chess.KING and missing[0].coords[0] == 4 and new[0].coords[0] in (2, 6):
                # Can't castle with just the king
                self.color_plays()
            elif self.board.is_en_passant(move):
                # Can't en passant without a detected capture
                self.color_plays()
            elif missing[0].piece.color == new[0].color:
                # Move
                return self.staging_move_piece(missing[0], new[0].coords)
            else:
                # A piece changed color while moving, doesn't make sense
                self.ui.update_move_screen(DataLib.icons.question, f"Unexpected\nboard state")

        elif missing_new_swaps == (1, 0, 1):
            if missing[0].piece.color == swaps[0].new_color:
                # Capture
                self.staging_remove_piece(swaps[0].coords) # Remove captured piece
                return self.staging_move_piece(missing[0], swaps[0].coords) # Move missing piece to capture position
            else:
                # Current player didn't perform a capture, the swap doesn't make sense
                self.ui.update_move_screen(DataLib.icons.question, f"Unexpected\nboard state")

        elif missing_new_swaps == (2, 1, 0):
            pawns = missing[0].piece.pieceType == chess.PAWN and missing[1].piece.pieceType == chess.PAWN
            different_colors = missing[0].piece.color != missing[1].piece.color
            correct_new_color = new[0].color == self.current_player
            if pawns and different_colors and correct_new_color:
                moving_pawn = None
                captured_pawn = None

                # En passant
                for piece in missing:
                    if piece.piece.color == self.current_player:
                        moving_pawn = piece
                    else:
                        captured_pawn = piece

                if moving_pawn and captured_pawn:
                    # En passant capture
                    self.staging_remove_piece(captured_pawn.coords)
                    return self.staging_move_piece(moving_pawn, new[0].coords)
                else:
                    self.ui.update_move_screen(DataLib.icons.question, f"Unexpected\nboard state")
            else:
                self.ui.update_move_screen(DataLib.icons.question, f"Unexpected\nboard state")

        elif missing_new_swaps == (2, 2, 0):
            king = None
            rook = None

            # Are missing king and rook?
            for miss in missing:
                if miss.piece.pieceType == chess.KING:
                    king = miss
                elif miss.piece.pieceType == chess.ROOK:
                    rook = miss

            if king is not None and rook is not None:
                color_check = king.piece.color == rook.piece.color == new[0].color == new[1].color
                king_check = king.coords[0] == 4 and king.coords[1] in (0, 7)
                rook_check = rook.coords[0] in (0, 7) and rook.coords[1] in (0, 7)
                king_dest = None
                rook_dest = None

                # Are new positions valid for castling?
                for new_pos in new:
                    if new_pos.coords[0] in (2, 6) and new_pos.coords[1] in (0, 7):
                        king_dest = new_pos
                    elif new_pos.coords[0] in (3, 5) and new_pos.coords[1] in (0, 7):
                        rook_dest = new_pos

                if color_check and king_check and rook_check and king_dest and rook_dest:
                    # Castling
                    self.staging_move_piece(rook, rook_dest.coords)
                    return self.staging_move_piece(king, king_dest.coords)
                else:
                    self.ui.update_move_screen(DataLib.icons.question, f"Unexpected\nboard state")
            else:
                self.ui.update_move_screen(DataLib.icons.question, f"Unexpected\nboard state")

        elif len(missing) > 1 or len(new) > 0 or len(swaps) > 0:
            # Generic fail
            self.ui.update_move_screen(DataLib.icons.question, f"Unexpected\nboard state")

        else:
            self.color_plays()

        return None

    def color_plays(self):
        if self.current_player == chess.WHITE:
            self.ui.update_move_screen(DataLib.icons.player_white, "White plays")
        else:
            self.ui.update_move_screen(DataLib.icons.player_black, "Black plays")

    def staging_move_piece(self, missing: MissingPiece, new_coords: tuple[int, int]):
        promotion = False
        if missing.piece.pieceType == chess.PAWN and new_coords[1] in (0, 7):
            promotion = True

        self.staging_state.pop(missing.coords)

        if promotion:
            # Remove pawn, add queen
            data = DataLib.pieces.white_queen if missing.piece.color == chess.WHITE else DataLib.pieces.black_queen
            self.staging_state[new_coords] = Piece(self, self.ui, data)
        else:
            self.staging_state[new_coords] = missing.piece

        # UCI
        uci = self.coords_to_locator(missing.coords) + self.coords_to_locator(new_coords)
        if promotion: uci += "q"
        return uci

    def staging_remove_piece(self, coords: tuple[int, int]):
        self.staging_state.pop(coords)

    def get_winner_string(self, winner: chess.Color | None):
        match winner:
            case chess.WHITE:
                return "White"
            case chess.BLACK:
                return "Black"
            case None:
                return "Draw"