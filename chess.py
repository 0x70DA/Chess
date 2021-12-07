"""
This file is responsible for storing all the information about the current state of the game.
It will also be responsible for determining the current available moves and keep a move log.
"""


class GameState():
    def __init__(self):
        self.board = [  # could use a numpy array to make it faster.
            ["black_rook", "black_knight", "black_bishop", "black_queen",
                "black_king", "black_bishop", "black_knight", "black_rook"],
            ["black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],  # -- represents an empty space on the board.
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn"],
            ["white_rook", "white_knight", "white_bishop", "white_queen",
                "white_king", "white_bishop", "white_knight", "white_rook"]
        ]
        self.white_to_move = True
        self.move_log = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # Log the move so that we can undo it later.
        self.white_to_move = not self.white_to_move  # switch players.


class Move():

    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}  # Row 7 -> rank 1
    rows_to_ranks = {value: key for key, value in ranks_to_rows.items()}  # Reverse the dictionary.
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}  # col 0 -> file a
    cols_to_files = {value: key for key, value in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        # In chess notation the file comes before the rank -> b6, g3.
        return self.cols_to_files[col] + self.rows_to_ranks[row]
