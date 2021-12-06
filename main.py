"""
This file is responsible for handeling user input and displaying the game.
"""

import pygame as pg
import chess

pg.init()  # Initialize pygame.
WIDTH = HEIGHT = 1024
DIMENSION = 8  # A chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}  # Store all the images in this global dictionary only one time at the start of the game.


def load_images():
    """Load the images into a global dictionary."""
    pieces = ["white_rook", "white_knight", "white_bishop", "white_queen", "white_king", "white_pawn",
              "black_rook", "black_knight", "black_bishop", "black_queen", "black_king", "black_pawn"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def main():
    """Handles the user input and updates the graphics."""
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = chess.GameState()
    load_images()
    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
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
