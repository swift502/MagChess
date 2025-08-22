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
    pass

class PieceLibrary:
    white_pawn: Icon
    white_rook: Icon
    white_knight: Icon
    white_bishop: Icon
    white_queen: Icon
    white_king: Icon

    black_pawn: Icon
    black_rook: Icon
    black_knight: Icon
    black_bishop: Icon
    black_queen: Icon
    black_king: Icon

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
