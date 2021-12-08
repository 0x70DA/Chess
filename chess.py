"""
This file is responsible for storing all the information about the current state of the game.
It will also be responsible for determining the current available moves and keep a move log.
"""


class GameState():
    def __init__(self):
        self.board = [  # could use a numpy array to make it faster.
            ["black_rook", "black_knight", "black_bishop", "black_queen",
                "black_King", "black_bishop", "black_knight", "black_rook"],
            ["black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],  # -- represents an empty space on the board.
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn"],
            ["white_rook", "white_knight", "white_bishop", "white_queen",
                "white_King", "white_bishop", "white_knight", "white_rook"]
        ]
        self.white_to_move = True
        self.move_log = []


    """ Takes a  move and excutes it. """
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # Log the move so that we can undo it later.
        self.white_to_move = not self.white_to_move  # switch players.

    """ An undo function to undo the last move. This function will be excuted on pressing 'z'. """
    def undo_move(self):
        if len(self.move_log) != 0: # Making sure there was a move to undo.
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved # Putting the piece back to its initial place.
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move # Switch players.

    
    """ All moves considering checks. """
    def get_valid_moves(self):
        return self.get_possible_moves()


    """ All moves whether valid or not. """
    def get_possible_moves(self):
        moves = []
        # Traversing the entire board.
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0] # Getting the color of the piece ('b' for black or 'w' for white or '-' for empty)
                if (turn == 'w' and self.white_to_move) and (turn == 'b' and not self.white_to_move):
                    piece = self.board[row][col][6] # getting the piece as ('r' for rook...etc.) notice 'K' for king and 'k' for knight.
                    # checking which piece we have then call the function that generates its possible moves.
                    if piece == 'p':
                        self.get_pawn_moves(row, col, moves)
                    elif piece == 'r':
                        self.get_rook_moves(row, col, moves)
                    elif piece == 'k':
                        self.get_knight_moves(row, col, moves)
                    elif piece == 'b':
                        self.get_bishop_moves(row, col, moves)
                    elif piece == 'q':
                        self.get_queen_moves(row, col, moves)
                    elif piece == 'K':
                        self.get_king_moves(row, col, moves)
        return moves

    # Get all pawn possible moves for the pawn in location row, col and add them to list.
    def get_pawn_moves(self, row, col, moves):
        pass


    # Get all rook possible moves for the rook in location row, col and add them to list.
    def get_rook_moves(self, row, col, moves):
        pass

    # Get all kinght possible moves for the knight in location row, col and add them to list.
    def get_knight_moves(self, row, col, moves):
        pass

    # Get all bishop possible moves for the bishop in location row, col and add them to list. 
    def get_bishop_moves(self, row, col, moves):
        pass

    # Get all queen possible moves for the queen in location row, col and add them to list.
    def get_queen_moves(self, row, col, moves):
        pass

    # Get all king possible moves for the king in location row, col and add them to list.
    def get_king_moves(self, row, col, moves):
        pass
  


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
        # Giving each move a unique ID ex: e2e4 -> 6444
        self.moveID =self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col 

    """ Overriding the equal method."""
    def __eq__(self, other):
        if isinstance(other, Move):  # Making sure that 'other' is an instance of Move to be able to compare to.
            return self.moveID == other.moveID
        return False


    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        # In chess notation the file comes before the rank -> b6, g3.
        return self.cols_to_files[col] + self.rows_to_ranks[row]
