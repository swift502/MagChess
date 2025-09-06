import asyncio
import chess
import flet as ft

from cell import Cell
from data import ColorSwap, DataLib, MissingPiece, NewPiece, IChessboard, BoardState, PieceLayout
from piece import Piece
from ui_instance import MagChessUI
from utilities import color_format

class Chessboard(IChessboard):
    game_over: bool = False
    flipped: bool = False

    state_stack: list[BoardState] = []
    staging_layout: PieceLayout
    spawned_pieces: list[Piece] = []

    cells: dict[tuple[int, int], Cell] = {}

    init_config: bool = False
    last_analysed_sensor_state: str | None

    @property
    def current_player(self):
        return self.state_stack[-1].player
    
    @property
    def next_player(self):
        return chess.WHITE if self.current_player == chess.BLACK else chess.BLACK

    def get_latest_board(self):
        if self.state_stack is None or len(self.state_stack) == 0:
            return None
        else:
            return self.state_stack[-1].board

    def locator_to_coords(self, locator: str):
        return (
            ord(locator[0]) - ord("a"),
            int(locator[1]) - 1
        )

    def coords_to_locator(self, coords: tuple[int, int]):
        return chr(coords[0] + ord("a")) + str(coords[1] + 1)

    def __init__(self, page: ft.Page, ui: MagChessUI):
        self.page = page
        self.ui = ui

        for co_letter in range(8):
            for co_number in range(8):
                self.cells[(co_letter, co_number)] = Cell((co_letter, co_number), ui)

    async def update(self):
        while True:
            # Board logic
            if not self.init_config and self.match_sensor_state("WW....BB" * 8):
                self.flipped = False
                self.init_game()
            elif not self.init_config and self.match_sensor_state("BB....WW" * 8):
                self.flipped = True
                self.init_game()
            elif not self.game_over:
                self.board_state_update()
                
            # Pieces
            for piece in self.spawned_pieces:
                piece.update()

            # Update
            self.ui.update()

            await asyncio.sleep(1/60)

    def update_sensor_value(self, coords: tuple[int, int], value: int):
        self.cells[coords].update(value)

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

        # Board
        board = chess.Board()

        # Pieces
        pieces = {}
        for locator, pieceData in DataLib.start_configuration().items():
            coords = self.locator_to_coords(locator)
            piece = Piece(self, self.ui, pieceData)
            pieces[coords] = piece

        # State
        init_state: BoardState = BoardState(board, pieces, chess.WHITE)
        self.state_stack.append(init_state)
        self.show_layout(pieces)

        self.last_analysed_sensor_state = None
        self.init_config = True
        
        print("New game detected")

    def clean_up(self):
        self.game_over = False

        # State
        self.state_stack = []
        self.staging_layout = {}

    def commit_staging_layout(self, move: chess.Move):
        board = self.state_stack[-1].board.copy()
        board.push(move)

        state = BoardState(board, self.staging_layout.copy(), self.next_player)
        self.state_stack.append(state)

        self.init_config = False

        print(f"Committed {move.uci()}")

    def show_layout(self, layout: PieceLayout):
        # Iterate state
        for coords, piece in layout.items():
            if piece in self.spawned_pieces:
                # Move existing
                piece.go_to(coords)
            else:
                # Spawn new
                piece.spawn(coords)

        # Remove obsolete
        for piece in self.spawned_pieces.copy():
            if piece not in layout.values():
                piece.destroy()

        self.ui.update_current_player()

    def board_state_update(self):
        if len(self.state_stack) == 0:
            return

        # Check for changes
        sensor_state = self.get_sensor_state_format()
        if self.last_analysed_sensor_state == sensor_state:
            return

        # Changes found, start new analysis
        self.last_analysed_sensor_state = sensor_state
        self.staging_layout = self.state_stack[-1].pieces.copy()
        illegal = False
        self.ui.hide_message()

        # Compare against current state
        missing_1, new_1, swaps_1 = self.analyse_sensor_changes(against=self.state_stack[-1])
        missing_new_swaps_1 = (len(missing_1), len(new_1), len(swaps_1))
        if missing_new_swaps_1 == (0, 0, 0):
            # Return to current state
            self.show_layout(self.staging_layout)
            return
        
        uci_1 = self.update_staging_state(missing_1, new_1, swaps_1, against=self.state_stack[-1])
        if uci_1 is not None:
            move = chess.Move.from_uci(uci_1)
            if move in self.state_stack[-1].board.legal_moves:
                # Made a valid move from current state
                self.process_move(move)
                self.show_layout(self.staging_layout)
                return
            else:
                illegal = True
            
        first_staging_layout = self.staging_layout.copy()
        
        # We didn't find valid moves from current state. Let's check if
        # the player returned a piece to its previous position or changed
        # their mind about what move they're making
        if len(self.state_stack) > 1:
            self.staging_layout = self.state_stack[-2].pieces.copy()

            # Compare against previous state
            missing_2, new_2, swaps_2 = self.analyse_sensor_changes(against=self.state_stack[-2])
            missing_new_swaps_2 = (len(missing_2), len(new_2), len(swaps_2))
            if missing_new_swaps_2 == (0, 0, 0):
                # Returned to previous state
                self.pop_state()
                self.show_layout(self.staging_layout)
                return
            
            uci_2 = self.update_staging_state(missing_2, new_2, swaps_2, against=self.state_stack[-2])
            if uci_2 is not None:
                move = chess.Move.from_uci(uci_2)
                if move in self.state_stack[-2].board.legal_moves:
                    # Made a valid move from the previous state
                    self.pop_state()
                    self.process_move(move)
                    self.show_layout(self.staging_layout)
                    return

        # Only found illegal or None
        # Give the best interpretation from the current state analysis
        if illegal:
            self.ui.board_state_info("Illegal move")
        elif len(missing_1) > 2 or len(new_1) > 1 or len(swaps_1) > 1:
            self.ui.board_state_info("Unexpected board state")
        elif missing_new_swaps_1 == (0, 0, 1):
            self.ui.board_state_info("Unexpected board state")
        
        self.show_layout(first_staging_layout)

    def process_move(self, move: chess.Move):
        self.commit_staging_layout(move)
        outcome = self.state_stack[-1].board.outcome()
        if outcome is not None:
            self.game_over = True
            self.ui.update_board_state(
                f"Game over! Winner: {color_format(outcome.winner)}",
                color=ft.Colors.BLACK,
                bgcolor="#dbac16",
            )

    def pop_state(self):
        self.state_stack.pop()
        print("Pop")

    def analyse_sensor_changes(self, against: BoardState):
        missing: list[MissingPiece] = []
        new: list[NewPiece] = []
        swaps: list[ColorSwap] = []

        # Find changes
        for coords, cell in self.cells.items():
            # Flipping
            if self.flipped:
                coords = (7 - coords[0], 7 - coords[1])

            # Get new color from sensor data
            new_color = cell.detected_color

            # Get old color from last committed state
            piece = against.pieces.get(coords)

            if piece is None:
                old_color = None

                # Found new
                if new_color is not None:
                    new.append(NewPiece(new_color, coords))

            else:
                old_color = piece.color

                # Found missing
                if new_color is None:
                    missing.append(MissingPiece(piece, coords))

                # Found swap
                elif old_color != new_color:
                    swaps.append(ColorSwap(piece, new_color, coords))

        return missing, new, swaps

    def update_staging_state(self, missing : list[MissingPiece], new: list[NewPiece], swaps: list[ColorSwap], against: BoardState) -> str | None:
        missing_new_swaps = (len(missing), len(new), len(swaps))

        if missing_new_swaps == (1, 1, 0):
            move = chess.Move.from_uci(self.coords_to_locator(missing[0].coords) + self.coords_to_locator(new[0].coords))
            if missing[0].piece.pieceType == chess.KING and missing[0].coords[0] == 4 and new[0].coords[0] in (2, 6):
                # Can't castle with just the king
                pass
            elif against.board.is_en_passant(move):
                # Can't en passant without a detected capture
                pass
            elif missing[0].piece.color == new[0].color:
                # Move
                return self.staging_move_piece(missing[0], new[0].coords)

        elif missing_new_swaps == (1, 0, 1):
            if missing[0].piece.color == swaps[0].new_color:
                # Capture
                self.staging_remove_piece(swaps[0].coords) # Remove captured piece
                return self.staging_move_piece(missing[0], swaps[0].coords) # Move missing piece to capture position

        elif missing_new_swaps == (2, 1, 0):
            pawns = missing[0].piece.pieceType == chess.PAWN and missing[1].piece.pieceType == chess.PAWN
            moving_pawn = None
            captured_pawn = None

            for miss in missing:
                if miss.piece.color == new[0].color:
                    moving_pawn = miss
                else:
                    captured_pawn = miss
            
            if pawns and moving_pawn and captured_pawn:
                move = chess.Move.from_uci(self.coords_to_locator(moving_pawn.coords) + self.coords_to_locator(new[0].coords))
                if against.board.is_en_passant(move):
                    # En passant
                    self.staging_remove_piece(captured_pawn.coords)
                    return self.staging_move_piece(moving_pawn, new[0].coords)

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
        
        return None

    def staging_move_piece(self, missing: MissingPiece, new_coords: tuple[int, int]):
        promotion = False
        if missing.piece.pieceType == chess.PAWN and new_coords[1] in (0, 7):
            promotion = True

        self.staging_layout.pop(missing.coords)

        if promotion:
            # Remove pawn, add queen
            data = DataLib.pieces.white_queen if missing.piece.color == chess.WHITE else DataLib.pieces.black_queen
            self.staging_layout[new_coords] = Piece(self, self.ui, data)
        else:
            self.staging_layout[new_coords] = missing.piece

        # UCI
        uci = self.coords_to_locator(missing.coords) + self.coords_to_locator(new_coords)
        if promotion:
            uci += "q"
        return uci

    def staging_remove_piece(self, coords: tuple[int, int]):
        self.staging_layout.pop(coords)
