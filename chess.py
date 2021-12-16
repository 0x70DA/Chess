"""
This file is responsible for storing all the information about the current state of the game.
It will also be responsible for determining the current available moves and keep a move log.
"""
from copy import deepcopy


class GameState():
    def __init__(self):
        # The first letter represents the color of the piece either (b)lack of (w)hite.
        # The second letter represents the piece (R->Rook, N->Knight, B->Bishop, Q->Queen, K->King, P->Pawn).
        # (--) represents an empty space on the board.
        self.board = [  # could use a numpy array to make it faster.
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        # A dictionary to map the getting moves functions to their right piece.
        self.get_moves_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                                    'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.white_to_move = True
        self.move_log = []
        # Keep track of the two kings' locations.
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        # To handle en passant.
        self.en_passant_possible = ()   # Coordinates for the possible square of enpassant.
        
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [deepcopy(self.current_castling_rights)]

    def make_move(self, move, promoted_pawn=""):
        """Takes a  move and excutes it."""
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # Log the move so that we can undo it later.
        self.white_to_move = not self.white_to_move  # switch players.
        # Update the king's location if moved.
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)
        # Pawn promotion.
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + promoted_pawn
        # En passant move.
        if move.is_en_passant:
            self.board[move.start_row][move.end_col] = '--'   # Capturing the pawn
        # Update the en_passant_possible field.
        if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:  # 2 square pawn advance.
            # The new location of the attacking pawn.
            self.en_passant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.en_passant_possible = ()   # Reset.

        # Castle move.
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:  # King side castle.
                # Move the left rook.
                self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1]
                self.board[move.end_row][move.end_col+1] = "--"  # Erase old rook.
            else:  # Queen side castling.
                # Move the left rook.
                self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2]
                self.board[move.end_row][move.end_col-2] = "--"  # Erase old rook.

        # Update castling rights whenever it's a rook or a king move.
        self.update_castle_rights(move)
        self.castle_rights_log.append(deepcopy(self.current_castling_rights))

    def undo_move(self):
        """An undo function to undo the last move. This function will be excuted on pressing 'z'."""
        if len(self.move_log) != 0:  # Making sure there was a move to undo.
            move = self.move_log.pop()
            # Putting the piece back to its initial place.
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move  # Switch players.
            # Update the king's location.
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

            # Undo en passant.
            if move.is_en_passant:
                self.board[move.end_row][move.end_col] = "--"   # Keeping the landing square empty.
                # Retruning the piece to its initial place.
                self.board[move.start_row][move.end_col] = move.piece_captured
                # Reset so we can redo the move after undoing the move.
                self.en_passant_possible = (move.end_row, move.end_col)
            # Undo a 2 square pawn advance. We have to reset the en_passant_possible field to ().
            if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:
                self.en_passant_possible = ()

            # Undo castling rights.
            self.castle_rights_log.pop()  # Get rid of the new casle rights from the move we are undoing.
            # set the current casle rights to the last one in the log.
            castle_rights = deepcopy(self.castle_rights_log[-1])
            self.current_castling_rights = castle_rights

            # Undo the castle move.
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # King side castling.
                    self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-1]
                    self.board[move.end_row][move.end_col-1] = "--"
                else:  # Queen side castling.
                    self.board[move.end_row][move.end_col-2] = self.board[move.end_row][move.end_col+1]
                    self.board[move.end_row][move.end_col+1] = "--"

            self.checkmate = False
            self.stalemate = False

            
    def update_castle_rights(self, move):
        """Update the castle rigths given the move."""
        # If the king is moved, all castling rights are lost.
        if move.piece_moved == 'wK':
            self.current_castling_rights.wks = False
            self.current_castling_rights.wqs = False
        elif move.piece_moved == 'bK':
            self.current_castling_rights.bks = False
            self.current_castling_rights.bqs = False
        elif move.piece_moved == 'wR' and move.start_row == 7:
            if move.start_col == 0:
                # Left rook moved.
                self.current_castling_rights.wqs = False
            elif move.start_col == 7:
                # Right rook moved.
                self.current_castling_rights.wks = False
        elif move.piece_moved == 'bR' and move.start_row == 0:
            if move.start_col == 0:
                # Left rook moved.
                self.current_castling_rights.bqs = False
            elif move.start_col == 7:
                # Right rook moved.
                self.current_castling_rights.bks = False
        # If a white rook was captured.
        elif move.piece_captured == 'wR':
            if move.end_row == 7:
                if move.end_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.wks = False
        # If a black rook was captured.
        elif move.piece_captured == 'bR':
            if move.end_row == 0:
                if move.end_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.bks = False

    def get_valid_moves(self):
        """All moves considering checks."""
        temp_enpassant_possible = self.en_passant_possible   # Saving the contents of the field so we can undo later.
        temp_castle_rights = deepcopy(self.current_castling_rights)  # Copy the current castling rights.
        # 1- Get all possible move.
        moves = self.get_possible_moves()

        # Get all castle moves.
        if self.white_to_move:
            self.get_castle_moves(*self.white_king_location, moves)
        else:
            self.get_castle_moves(*self.black_king_location, moves)

        # 2- For each move, make the move.
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i])  # This function switchs turns.
            # 3- Get all opponent's moves.
            # 4- For each of the opponent's move, see if they attack your king.
            self.white_to_move = not self.white_to_move  # Switch the turns to see if the king is in check.
            if self.in_check():
                # 5- If they do attack your king, then it's not a valid move.
                moves.remove(moves[i])
            # Switch the turns back to its original state before calling in_check().
            self.white_to_move = not self.white_to_move
            self.undo_move()
        if len(moves) == 0:
            # Either a checkmate or a stalemate.
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            # Switch these flags back in case we needed to undo a move that had resulted in either of them.
            self.checkmate = False
            self.stalemate = False

        # Restoring the contents after being changed in calling make_move.
        self.en_passant_possible = temp_enpassant_possible
        self.current_castling_rights = temp_castle_rights
        return moves

    def in_check(self):
        """"Determine if the player is in check."""
        if self.white_to_move:
            return self.square_under_attack(*self.white_king_location)
        else:
            return self.square_under_attack(*self.black_king_location)

    def square_under_attack(self, row, col):
        """Determine if the enemy can attack a specific square."""
        self.white_to_move = not self.white_to_move  # Switch to the opponent's point of view.
        opponent_moves = self.get_possible_moves()
        self.white_to_move = not self.white_to_move  # Switch the turns back.
        for move in opponent_moves:
            if move.end_row == row and move.end_col == col:
                # The square is under attack.
                return True
        return False

    def get_possible_moves(self):
        """All moves whether valid or not."""
        moves = []
        # Traversing the entire board.
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                # Getting the color of the piece ('b' for black or 'w' for white or '-' for empty)
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    # Get the second character as the name of the piece.
                    piece = self.board[row][col][1]
                    # Calling the function that generates the piece's possible moves.
                    self.get_moves_functions[piece](row, col, moves)
        return moves

    def get_pawn_moves(self, row, col, moves):
        """Get all pawn possible moves for the pawn in location row, col and add them to moves list."""
        # White pawns moves.
        if self.white_to_move:  # Checking if it's white's turn to move.
            if self.board[row - 1][col] == '--':  # 1 square pawn advance.
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == '--':  # 2 square pawn advance.
                    moves.append(Move((row, col), (row - 2, col), self.board))
            # White pawns captures. "Pawns can only capture diagonally one square to the right or the left."
            if col - 1 >= 0:  # Making sure that we don't have any negative numbers.
                # Capturing a black piece to the left.
                if self.board[row - 1][col - 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
                # Tells the engine this is an en passant move.
                elif (row - 1, col - 1) == self.en_passant_possible:
                    moves.append(Move((row, col), (row - 1, col - 1), self.board, is_en_passant=True))

            if col + 1 <= 7:  # Making sure we don't cross the borders of the board
                # Capturing a black piece to the right
                if self.board[row - 1][col + 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
                # Tells the engine this is an en passant move.
                elif (row - 1, col + 1) == self.en_passant_possible:
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, is_en_passant=True))

        # Black pawns moves.
        else:
            if self.board[row + 1][col] == '--':
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '--':
                    moves.append(Move((row, col), (row + 2, col), self.board))
            # Black pawns captures.
            if col - 1 >= 0:  # Making sure that we don't have any negative numbers.
                # Capturing a white piece to the left.
                if self.board[row + 1][col - 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
                # Tells the engine this is an en passant move.
                elif (row + 1, col - 1) == self.en_passant_possible:
                    moves.append(Move((row, col), (row + 1, col - 1), self.board, is_en_passant=True))

            if col + 1 <= 7:  # Making sure we don't cross the borders of the board.
                # Capturing a white piece to the right
                if self.board[row + 1][col + 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
                # Tells the engine this is an en passant move.
                elif (row + 1, col + 1) == self.en_passant_possible:
                    moves.append(Move((row, col), (row + 1, col + 1), self.board, is_en_passant=True))

    def get_rook_moves(self, row, col, moves):
        """Get all rook possible moves for the rook in location row, col and add them to the move list."""
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Moving (up, left, down, right).
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):  # A rook can move one square in the four directions up to seven squares.
                end_row = row + i * d[0]
                end_col = col + i * d[1]
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # The piece is still in the board.
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        # Capture enemy piece.
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        # Friendly piece, invalid move.
                        break
                else:
                    # Off board.
                    break

    # Get all kinght possible moves for the knight in location row, col and add them to list.

    def get_knight_moves(self, row, col, moves):
        """Get all knight possible moves for the knight in location row, col and add them to the move list."""
        knight_moves = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, 2), (1, 2), (-1, -2), (1, -2)
                        )  # All posiible moves for a knight.
        enemy_color = "b" if self.white_to_move else "w"
        for m in knight_moves:
            end_row = row + m[0]
            end_col = col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] == enemy_color:
                    # Move to empty space or capture enmey piece.
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    # Get all bishop possible moves for the bishop in location row, col and add them to list.

    def get_bishop_moves(self, row, col, moves):
        """Get all bishop possible moves for the bishop in location row, col and add them to the move list."""
        directions = ((-1, -1), (1, -1), (1, 1), (-1, 1))  # Moving diagonally.
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):  # A bishop can move diagonally one square in the four directions up to seven squares.
                end_row = row + i * d[0]
                end_col = col + i * d[1]
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # The piece is still in the board.
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        # Capture enemy piece.
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        # Friendly piece, invalid move.
                        break
                else:
                    # Off board.
                    break

    # Get all queen possible moves for the queen in location row, col and add them to list.
    def get_queen_moves(self, row, col, moves):
        """Get all queen possible moves for the queen in location row, col and add them to the move list."""
        # Queen moves are a combination of the rook moves and the bishop moves.
        self.get_bishop_moves(row, col, moves)
        self.get_rook_moves(row, col, moves)

    # Get all king possible moves for the king in location row, col and add them to list.
    def get_king_moves(self, row, col, moves):
        """Get all king possible moves for the king in location row, col and add them to the move list."""
        # The king can move in any direction, but only one square.
        king_moves = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = "b" if self.white_to_move else "w"
        for i in range(8):
            end_row = row + king_moves[i][0]
            end_col = col + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] == enemy_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_castle_moves(self, row, col, moves):
        """Get all valid castling moves for the king at (row, col) and add them to the list of moves."""
        if self.square_under_attack(row, col):
            # You can't castle while in check!
            return
        if (self.white_to_move and self.current_castling_rights.wks) or (not self.white_to_move and self.current_castling_rights.bks):
            self.king_side_castle_moves(row, col, moves)
        if (self.white_to_move and self.current_castling_rights.wqs) or (not self.white_to_move and self.current_castling_rights.bqs):
            self.queen_side_castle_moves(row, col, moves)

    def king_side_castle_moves(self, row, col, moves):
        if self.board[row][col+1] == "--" and self.board[row][col+2] == "--":
            if not self.square_under_attack(row, col+1) and not self.square_under_attack(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, is_castle_move=True))

    def queen_side_castle_moves(self, row, col, moves):
        if self.board[row][col-1] == "--" and self.board[row][col-2] == "--" and self.board[row][col-3] == "--":
            if not self.square_under_attack(row, col-1) and not self.square_under_attack(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, is_castle_move=True))


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):  # white king side, black king side,...
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():

    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}  # Row 7 -> rank 1
    rows_to_ranks = {value: key for key, value in ranks_to_rows.items()}  # Reverse the dictionary.
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}  # col 0 -> file a
    cols_to_files = {value: key for key, value in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, is_en_passant=False, is_castle_move=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # Giving each move a unique ID ex: e2e4 -> 6444
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

        # To handle pawn promotion.
        self.is_pawn_promotion = ((self.piece_moved == 'wP' and self.end_row == 0) or
                                  (self.piece_moved == 'bP' and self.end_row == 7))

        # To handle en passant.
        self.is_en_passant = is_en_passant
        if self.is_en_passant:
            self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"

        # Handle castling.
        self.is_castle_move = is_castle_move

    def __eq__(self, other):
        """Overriding the equal method."""
        if isinstance(other, Move):  # Making sure that 'other' is an instance of Move to be able to compare to.
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        # In chess notation the file comes before the rank -> b6, g3.
        return self.cols_to_files[col] + self.rows_to_ranks[row]
