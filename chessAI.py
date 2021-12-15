import random

PIECE_SCORE = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000  # Highest score.
STALEMATE = 0  # Better than losing, but not as good as checkmate.


def find_random_move(valid_moves):
    """Return a random move from the list of valid moves."""
    return random.choice(valid_moves)


def find_best_move(gs, valid_moves):
    """Find the best move based only on material using a greedy approach."""
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_min_max_score = CHECKMATE  # The minimum of all the maximum scores that the opponent has.
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        gs.make_move(player_move, promoted_pawn='Q')
        opponent_moves = gs.get_valid_moves()
        opponent_max_score = -CHECKMATE
        for opponent_move in opponent_moves:
            gs.make_move(opponent_move, promoted_pawn='Q')
            if gs.checkmate:
                score = -turn_multiplier * CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
            else:
                score = -turn_multiplier * score_material(gs.board)
            if score > opponent_max_score:
                opponent_max_score = score
            gs.undo_move()
        if opponent_max_score < opponent_min_max_score:
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()
    return best_player_move


def score_material(board):
    """Score the board based on material alone not considering the position."""
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                # For white to win the score need to be a positive value.
                # Meaning that white is trying to maximize the score.
                score += PIECE_SCORE[square[1]]
            elif square[0] == 'b':
                # Black is trying to minimize the score.
                score -= PIECE_SCORE[square[1]]
    return score
