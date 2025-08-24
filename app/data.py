from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING

from enums import ChessColor

if TYPE_CHECKING:
    from piece import Piece

class IconData:
    def __init__(self, path: str, color: str):
        self.image_path = path
        self.color = color

class IconLibrary:
    def __init__(self):
        self.alternative = IconData(path="icons/alternative.svg", color="#96af8b")
        self.best = IconData(path="icons/best.svg", color="#96bc4b")
        self.blunder = IconData(path="icons/blunder.svg", color="#ca3431")
        self.book = IconData(path="icons/book.svg", color="#a88865")
        self.brilliant = IconData(path="icons/brilliant.svg", color="#1bada6")
        self.checkmate_black = IconData(path="icons/checkmate_black.svg", color="#312e2b")
        self.checkmate_white = IconData(path="icons/checkmate_white.svg", color="#f8f8f8")
        self.correct = IconData(path="icons/correct.svg", color="#96bc4b")
        self.critical = IconData(path="icons/critical.svg", color="#ad5b8c")
        self.draw_black = IconData(path="icons/draw_black.svg", color="#312e2b")
        self.draw_white = IconData(path="icons/draw_white.svg", color="#f8f8f8")
        self.excellent = IconData(path="icons/excellent.svg", color="#96bc4b")
        self.fast_win = IconData(path="icons/fast_win.svg", color="#96af8b")
        self.forced = IconData(path="icons/forced.svg", color="#96af8b")
        self.free_piece = IconData(path="icons/free_piece.svg", color="#ec6250")
        self.good = IconData(path="icons/good.svg", color="#96af8b")
        self.great_find = IconData(path="icons/great_find.svg", color="#96af8b")
        self.inaccuracy = IconData(path="icons/inaccuracy.svg", color="#f7c045")
        self.incorrect = IconData(path="icons/incorrect.svg", color="#ca3431")
        self.invalid = IconData(path="icons/invalid.svg", color="#7979a1")
        self.mate = IconData(path="icons/mate.svg", color="#ec6250")
        self.missed_win = IconData(path="icons/missed_win.svg", color="#dbac16")
        self.mistake = IconData(path="icons/mistake.svg", color="#e58f2a")
        self.player_black = IconData(path="icons/player_black.svg", color="#383838")
        self.player_white = IconData(path="icons/player_white.svg", color="#ebebeb")
        self.question = IconData(path="icons/question.svg", color="#7979a1")
        self.search = IconData(path="icons/search.svg", color="#7979a1")
        self.sharp = IconData(path="icons/sharp.svg", color="#ad5b8c")
        self.take_back = IconData(path="icons/take_back.svg", color="#96af8b")
        self.threat = IconData(path="icons/threat.svg", color="#96af8b")
        self.winner = IconData(path="icons/winner.svg", color="#dbac16")

class PieceData:
    def __init__(self, path: str, color: ChessColor):
        self.image_path = path
        self.color = color

class NewPiece:
    def __init__(self, color: ChessColor, coords: tuple[int, int]):
        self.color = color
        self.coords = coords

class MissingPiece:
    def __init__(self, piece: Piece, coords: tuple[int, int]):
        self.piece = piece
        self.coords = coords

class ColorSwap:
    def __init__(self, old_piece: Piece, new_color: ChessColor, coords: tuple[int, int]):
        self.old_piece = old_piece
        self.new_color = new_color
        self.coords = coords

class PieceLibrary:
    def __init__(self):
        self.white_pawn = PieceData(path="pieces/pawn_white.svg", color=ChessColor.WHITE)
        self.white_rook = PieceData(path="pieces/rook_white.svg", color=ChessColor.WHITE)
        self.white_knight = PieceData(path="pieces/knight_white.svg", color=ChessColor.WHITE)
        self.white_bishop = PieceData(path="pieces/bishop_white.svg", color=ChessColor.WHITE)
        self.white_queen = PieceData(path="pieces/queen_white.svg", color=ChessColor.WHITE)
        self.white_king = PieceData(path="pieces/king_white.svg", color=ChessColor.WHITE)

        self.black_pawn = PieceData(path="pieces/pawn_black.svg", color=ChessColor.BLACK)
        self.black_rook = PieceData(path="pieces/rook_black.svg", color=ChessColor.BLACK)
        self.black_knight = PieceData(path="pieces/knight_black.svg", color=ChessColor.BLACK)
        self.black_bishop = PieceData(path="pieces/bishop_black.svg", color=ChessColor.BLACK)
        self.black_queen = PieceData(path="pieces/queen_black.svg", color=ChessColor.BLACK)
        self.black_king = PieceData(path="pieces/king_black.svg", color=ChessColor.BLACK)

class DataLib:
    icons = IconLibrary()
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

class SensorProvider:
    def __init__(self) -> None:
        raise NotImplementedError()

    def get_value_array(self) -> dict[tuple[int, int], float]:
        raise NotImplementedError()

    def cycle_sensor_state(self, co_letter: int, co_number: int) -> None:
        raise NotImplementedError()
