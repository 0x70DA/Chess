"""
This file is responsible for handeling user input and displaying the game.
"""

import pygame as pg
import chess
import chessAI
import random

pg.init()  # Initialize pygame.
WIDTH = HEIGHT = 512
DIMENSION = 8  # A chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}  # Store all the images in this global dictionary only one time at the start of the game.


def load_images():
    """Load the images into a global dictionary."""
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def main():
    """Handles the user input and updates the graphics."""
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = chess.GameState()
    valid_moves = gs.get_valid_moves()  # A list to check the valid moves we have and act on them.
    promoted_pawn = ""
    animate = False   # A flag for animation.
    move_made = False  # A variable based on we will be generating new valid moves for the new piece.
    game_over = False
    load_images()
    running = True
    # No square is selected initially. This will keep track of the last click of the user -> (row, col).
    sq_selected = ()
    # Keep track of the player clicks. This list will contain two tuples the first is the starting pos and the second is the ending pos.
    player_clicks = []

    # Create two variables to indicate whether a Human or an AI is playing.
    # If a Human is playing the variable will be set to Ture, if an AI is playing it will be set to False.
    player_one = True  # This is for the white player.
    player_two = False  # For the black player.
    while running:
        is_human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            # Mouse handler
            elif e.type == pg.MOUSEBUTTONDOWN:
                # Allow mouse clicks only if it's a Human player's turn.
                if not game_over and is_human_turn:
                    location = pg.mouse.get_pos()  # (x,y) posiotion of the mouse.
                    col = location[0] // SQ_SIZE  # The x coordinate.
                    row = location[1] // SQ_SIZE  # The y coordinate.
                    if sq_selected == (row, col):
                        # If the user selected the same square twice, deselect that square.
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)

                    if len(player_clicks) == 2:
                        # After the second click.
                        move = chess.Move(player_clicks[0], player_clicks[1], gs.board)
                        print(move.get_chess_notation())  # for debugging.
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:  # Only make a valid move for this piece.
                                if move.is_pawn_promotion:
                                    promoted_pawn = input("promote to Q, R, B, N: ")
                                gs.make_move(valid_moves[i], promoted_pawn)
                                move_made = True  # Raising a flag that a valid move was made.
                                animate = True
                                # Reset user clicks.
                                sq_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]
            # Key handler
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:  # On pressing the button 'z' on keyboard.
                    gs.undo_move()
                    move_made = True  # will be important in the Ai creation later on.
                    animate = False
                    game_over = False
                # Resetting the game.
                if e.key == pg.K_r:
                    gs = chess.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    promoted_pawn = ""
                    game_over = False

        # AI move finder.
        if not game_over and not is_human_turn:
            ai_move = chessAI.find_best_move(gs, valid_moves)
            # In case the algorithm can't find the best move, choose a random move.
            if ai_move == None:
                ai_move = chessAI.find_random_move(valid_moves)

            if ai_move.is_pawn_promotion:
                promoted_pawn = 'Q'

            gs.make_move(ai_move, promoted_pawn)
            move_made = True
            animate = True

        # Only generate new list of valid moves if a valid move was made.
        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)   # Animate the last move in the move log.
            valid_moves = gs.get_valid_moves()
            move_made = False  # Reset the flag.
            animate = False

        draw_game_state(screen, gs, valid_moves, sq_selected)

        if gs.checkmate:
            game_over = True
            if gs.white_to_move:
                draw_text(screen, 'Black wins by checkmate!')
            else:
                draw_text(screen, 'White wins by checkmate!')
        elif gs.stalemate:
            game_over = True
            draw_text(screen, 'Stalemate!')

        clock.tick(MAX_FPS)
        pg.display.flip()


def highlight_squares(screen, gs, valid_moves, sq_selected):
    """Highlight square selected and the valid moves for the piece."""
    if sq_selected != ():   # Making sure we selected a square.
        row, col = sq_selected
        # Making sure we selected a piece that can be moved.
        if gs.board[row][col][0] == ('w' if gs.white_to_move else 'b'):
            # Highlight the selected square.
            surface = pg.Surface((SQ_SIZE, SQ_SIZE))
            surface.set_alpha(100)   # Tranperancy value.
            surface.fill(pg.Color('blue'))
            screen.blit(surface, (col*SQ_SIZE, row*SQ_SIZE))
            # Highlight moves from that square.
            surface.fill(pg.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(surface, (SQ_SIZE*move.end_col, SQ_SIZE*move.end_row))


def draw_game_state(screen, gs, valid_moves, sq_selected):
    """Draws the squares on the board and puts the pieces on that board."""
    draw_board(screen)
    # Highlight.
    highlight_squares(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    """Draw the squares on the board. The top left square is always white."""
    global colors
    colors = [pg.Color("white"), pg.Color("grey")]
    # For all white squares the sum of the row number and the column number is always even. (0,0) (0,2)
    # Whereas for dark squares the sum is always odd. (0,1) (0,3)
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row+col) % 2)]
            pg.draw.rect(screen, color, pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    """Draws the pieces on the board using the current game state board."""
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animate_move(move, screen, board, clock):
    global colors
    delta_row = move.end_row - move.start_row
    delta_col = move.end_col - move.start_col
    frames_per_square = 1   # Frames to move one square.
    frame_count = (abs(delta_row) + abs(delta_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + delta_row*frame/frame_count, move.start_col + delta_col*frame/frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        # Erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = pg.Rect(move.end_col*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pg.draw.rect(screen, color, end_square)
        # Draw captured piece onto rectangle.
        if move.piece_captured != '--':
            screen.blit(IMAGES[move.piece_captured], end_square)
        # Draw the moving piece.
        screen.blit(IMAGES[move.piece_moved], pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pg.display.flip()
        clock.tick(60)


def draw_text(screen, text):
    font = pg.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, 0, pg.Color('red'))
    text_location = pg.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH/2 - text_object.get_width()/2, HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, pg.Color('Black'))
    screen.blit(text_object, text_location.move(2, 2))


if __name__ == "__main__":
    main()
