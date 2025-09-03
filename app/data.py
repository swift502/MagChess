from typing import TypeAlias
import chess

from piece import Piece

class PieceData:
    def __init__(self, path: str, color: chess.Color, pieceType: chess.PieceType):
        self.image_path = path
        self.color = color
        self.pieceType = pieceType

class NewPiece:
    def __init__(self, color: chess.Color, coords: tuple[int, int]):
        self.color = color
        self.coords = coords

class MissingPiece:
    def __init__(self, piece: Piece, coords: tuple[int, int]):
        self.piece = piece
        self.coords = coords

class ColorSwap:
    def __init__(self, old_piece: Piece, new_color: chess.Color, coords: tuple[int, int]):
        self.old_piece = old_piece
        self.new_color = new_color
        self.coords = coords

class PieceLibrary:
    def __init__(self):
        self.white_pawn = PieceData(path="pieces/pawn_white.svg", color=chess.WHITE, pieceType=chess.PAWN)
        self.white_rook = PieceData(path="pieces/rook_white.svg", color=chess.WHITE, pieceType=chess.ROOK)
        self.white_knight = PieceData(path="pieces/knight_white.svg", color=chess.WHITE, pieceType=chess.KNIGHT)
        self.white_bishop = PieceData(path="pieces/bishop_white.svg", color=chess.WHITE, pieceType=chess.BISHOP)
        self.white_queen = PieceData(path="pieces/queen_white.svg", color=chess.WHITE, pieceType=chess.QUEEN)
        self.white_king = PieceData(path="pieces/king_white.svg", color=chess.WHITE, pieceType=chess.KING)

        self.black_pawn = PieceData(path="pieces/pawn_black.svg", color=chess.BLACK, pieceType=chess.PAWN)
        self.black_rook = PieceData(path="pieces/rook_black.svg", color=chess.BLACK, pieceType=chess.ROOK)
        self.black_knight = PieceData(path="pieces/knight_black.svg", color=chess.BLACK, pieceType=chess.KNIGHT)
        self.black_bishop = PieceData(path="pieces/bishop_black.svg", color=chess.BLACK, pieceType=chess.BISHOP)
        self.black_queen = PieceData(path="pieces/queen_black.svg", color=chess.BLACK, pieceType=chess.QUEEN)
        self.black_king = PieceData(path="pieces/king_black.svg", color=chess.BLACK, pieceType=chess.KING)

class DataLib:
    pieces = PieceLibrary()

    @staticmethod
    def start_configuration():
        return {
            "a1": DataLib.pieces.white_rook,
            "b1": DataLib.pieces.white_knight,
            "c1": DataLib.pieces.white_bishop,
            "d1": DataLib.pieces.white_queen,
            "e1": DataLib.pieces.white_king,
            "f1": DataLib.pieces.white_bishop,
            "g1": DataLib.pieces.white_knight,
            "h1": DataLib.pieces.white_rook,
            "a2": DataLib.pieces.white_pawn,
            "b2": DataLib.pieces.white_pawn,
            "c2": DataLib.pieces.white_pawn,
            "d2": DataLib.pieces.white_pawn,
            "e2": DataLib.pieces.white_pawn,
            "f2": DataLib.pieces.white_pawn,
            "g2": DataLib.pieces.white_pawn,
            "h2": DataLib.pieces.white_pawn,
            "a7": DataLib.pieces.black_pawn,
            "b7": DataLib.pieces.black_pawn,
            "c7": DataLib.pieces.black_pawn,
            "d7": DataLib.pieces.black_pawn,
            "e7": DataLib.pieces.black_pawn,
            "f7": DataLib.pieces.black_pawn,
            "g7": DataLib.pieces.black_pawn,
            "h7": DataLib.pieces.black_pawn,
            "a8": DataLib.pieces.black_rook,
            "b8": DataLib.pieces.black_knight,
            "c8": DataLib.pieces.black_bishop,
            "d8": DataLib.pieces.black_queen,
            "e8": DataLib.pieces.black_king,
            "f8": DataLib.pieces.black_bishop,
            "g8": DataLib.pieces.black_knight,
            "h8": DataLib.pieces.black_rook,
        }

PieceLayout: TypeAlias = dict[tuple[int, int], Piece]

class BoardState:
    pieces: PieceLayout
    board: chess.Board
    player: chess.Color

    def __init__(self, board: chess.Board, pieces: PieceLayout, player: chess.Color):
        self.board = board
        self.pieces = pieces
        self.player = player

    def copy(self):
        new_state = BoardState(self.board.copy(), self.pieces.copy(), self.player)
        return new_state

class IChessboard:
    game_over: bool

    @property
    def current_player(self) -> chess.Color:
        raise NotImplementedError()

    def get_latest_board(self) -> chess.Board | None:
        raise NotImplementedError()
