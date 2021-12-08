"""
This file is responsible for handeling user input and displaying the game.
"""

import pygame as pg
import chess

pg.init()  # Initialize pygame.
WIDTH = HEIGHT = 512
DIMENSION = 8  # A chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}  # Store all the images in this global dictionary only one time at the start of the game.


def load_images():
    """Load the images into a global dictionary."""
    pieces = ["white_rook", "white_knight", "white_bishop", "white_queen", "white_King", "white_pawn",
              "black_rook", "black_knight", "black_bishop", "black_queen", "black_King", "black_pawn"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def main():
    """Handles the user input and updates the graphics."""
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = chess.GameState()
    valid_moves = gs.get_valid_moves() # A list to check the valid moves we have and act on them.
    move_made = False # A variable based on we will be generating new valid moves for the new piece.
    load_images()
    running = True
    # No square is selected initially. This will keep track of the last click of the user -> (row, col).
    sq_selected = ()
    # Keep track of the player clicks. This list will contain two tuples the first is the starting pos and the second is the ending pos.
    player_clicks = []
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            # Mouse handler
            elif e.type == pg.MOUSEBUTTONDOWN:
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
                    if move in valid_moves: # Only make a valid move for this piece.
                        gs.make_move(move)
                        move_made = True  # Rising a flag to that a valid move was made.
                    # Reset user clicks.
                    sq_selected = ()
                    player_clicks = []
            # Key handler
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z: # On pressing the button 'z' on keyboard.
                    gs.undo_move()
                    move_made = True # will be important in the Ai creation later on.

        # Only generate new list of valid moves if a valid move was made.
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False # Reset the flag.

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        pg.display.flip()


def draw_game_state(screen, gs):
    """Draws the squares on the board and puts the pieces on that board."""
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    """Draw the squares on the board. The top left square is always white."""
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


if __name__ == "__main__":
    main()
