"""
This file is responsible for storing all the information about the current state of the game.
It will also be responsible for determining the current available moves and keep a move log.
"""


class GameState():
    def __init__(self):
        self.board = [  # could use a numpy array to make it faster.
            ["black_rook", "black_knight", "black_bishop", "black_queen", "black_king", "black_bishop", "black_knight", "black_rook"],
            ["black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],  # -- represents an empty space on the board.
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn"],
            ["white_rook", "white_knight", "white_bishop", "white_queen", "white_king", "white_bishop", "white_knight", "white_rook"]
        ]
        self.white_to_move = True
        self.move_log = []
