from pathlib import Path

class Icon:
    path: str
    color: str

    def __init__(self, path: str, color: str):
        self.path = path
        self.color = color

    def get_path(self):
        return str(Path(__file__).parent / "assets" / self.path)

class IconLibrary:
    def __init__(self):
        self.alternative = Icon(path="icons/alternative.svg", color="#96af8b")
        self.best = Icon(path="icons/best.svg", color="#96bc4b")
        self.blunder = Icon(path="icons/blunder.svg", color="#ca3431")
        self.book = Icon(path="icons/book.svg", color="#a88865")
        self.brilliant = Icon(path="icons/brilliant.svg", color="#1bada6")
        self.checkmate_black = Icon(path="icons/checkmate_black.svg", color="#312e2b")
        self.checkmate_white = Icon(path="icons/checkmate_white.svg", color="#f8f8f8")
        self.correct = Icon(path="icons/correct.svg", color="#96bc4b")
        self.critical = Icon(path="icons/critical.svg", color="#ad5b8c")
        self.draw_black = Icon(path="icons/draw_black.svg", color="#312e2b")
        self.draw_white = Icon(path="icons/draw_white.svg", color="#f8f8f8")
        self.excellent = Icon(path="icons/excellent.svg", color="#96bc4b")
        self.fast_win = Icon(path="icons/fast_win.svg", color="#96af8b")
        self.forced = Icon(path="icons/forced.svg", color="#96af8b")
        self.free_piece = Icon(path="icons/free_piece.svg", color="#ec6250")
        self.good = Icon(path="icons/good.svg", color="#96af8b")
        self.great_find = Icon(path="icons/great_find.svg", color="#96af8b")
        self.inaccuracy = Icon(path="icons/inaccuracy.svg", color="#f7c045")
        self.incorrect = Icon(path="icons/incorrect.svg", color="#ca3431")
        self.mate = Icon(path="icons/mate.svg", color="#ec6250")
        self.missed_win = Icon(path="icons/missed_win.svg", color="#dbac16")
        self.mistake = Icon(path="icons/mistake.svg", color="#e58f2a")
        self.sharp = Icon(path="icons/sharp.svg", color="#ad5b8c")
        self.take_back = Icon(path="icons/take_back.svg", color="#96af8b")
        self.threat = Icon(path="icons/threat.svg", color="#96af8b")
        self.winner = Icon(path="icons/winner.svg", color="#dbac16")

class PieceLibrary:
    def __init__(self):
        self.white_pawn = Icon(path="pieces/pawn_white.svg", color="#f8f8f8")
        self.white_rook = Icon(path="pieces/rook_white.svg", color="#f8f8f8")
        self.white_knight = Icon(path="pieces/knight_white.svg", color="#f8f8f8")
        self.white_bishop = Icon(path="pieces/bishop_white.svg", color="#f8f8f8")
        self.white_queen = Icon(path="pieces/queen_white.svg", color="#f8f8f8")
        self.white_king = Icon(path="pieces/king_white.svg", color="#f8f8f8")

        self.black_pawn = Icon(path="pieces/pawn_black.svg", color="#565352")
        self.black_rook = Icon(path="pieces/rook_black.svg", color="#565352")
        self.black_knight = Icon(path="pieces/knight_black.svg", color="#565352")
        self.black_bishop = Icon(path="pieces/bishop_black.svg", color="#565352")
        self.black_queen = Icon(path="pieces/queen_black.svg", color="#565352")
        self.black_king = Icon(path="pieces/king_black.svg", color="#565352")

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
