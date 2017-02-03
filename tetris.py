# Second attempt at tetris clone
# Tetris clone

# TODO
# 1. Rotate using spacebar
# 2. Stop when the piece is blocked by lower pieces - DONE
# 3. Clear the line if we have a full line
# 4. Look into scoring
# 5. Drop instantly using K_DOWN
# 6. Show outline of where the piece is due to land
# 7. Implement levels
# 8. Implement a high score system
# 9. End if the top layer isn't clear
# 10. Start with a spacebar

import pygame
import math
import random
import numpy as np

XMAX=700
YMAX=750
BLOCK_SIZE=30 # will try this for now, means the game grid will be 300 wide and 600 tall as we need 20x10 blocks
# The grid will go from [50,100] to [350,700]
START=[ 50 + 3*BLOCK_SIZE , 10 ] # the top left corner starts here (outside the grid), but we'll only print the pieces as they come into the grid
RIGHT_EDGE=350
LEFT_EDGE=50 # can softcode these in later but for now it's fine
UPPER_EDGE=100
LOWER_EDGE=700

class Shape:

    def __init__ (self,shape):

        self.shape = shape
        self.x    = START[0] # initialise the piece at the top - this is the top left piece in the 4x4 (or 3x3) square
        self.y    = START[1]

# We're going to have 7 different possible shapes, characterised by the variable "shape":
# 1 = square, 2 = line, 3 = S, 4 = Z, 5 = T, 6 = L, 7 = backwards L
        if shape == 1 :
            self.piece_matrix = [ [0,0,0,0], [0,1,1,0], [0,1,1,0], [0,0,0,0] ] # no rotation (or 4x4)
            self.colour       = RED
        elif shape == 2:
            self.piece_matrix = [ [0,0,0,0], [0,0,0,0], [1,1,1,1], [0,0,0,0] ] # 4x4 rotation
            self.colour       = BLUE
        elif shape == 3:
            self.piece_matrix = [ [0,0,0], [1,1,0], [0,1,1] ] # 3x3 rotation 
            self.colour       = GREEN
        elif shape == 4:
            self.piece_matrix = [ [0,0,0], [0,1,1], [1,1,0] ] # same for all below
            self.colour       = YELLOW
        elif shape == 5:
            self.piece_matrix = [ [0,0,0], [1,1,1], [0,1,0] ]
            self.colour       = PURPLE
        elif shape == 6: 
            self.piece_matrix = [ [0,0,0], [1,1,1], [1,0,0] ]
            self.colour       = ORANGE
        elif shape == 7:
            self.piece_matrix = [ [0,0,0], [1,1,1], [0,0,1] ]
            self.colour       = CYAN

    def rotate(self):
        self.piece_matrix = zip(*self.piece_matrix) # Take the transpose, but now they are given in tuples, so we will have to map(list, matrix)
        self.piece_matrix = map ( list , self.piece_matrix )[::-1] # turn it back into lists, and then write backwards. This gives the matrix rotated 90degrees anticlockwise

    def drop_one(self):
        self.y+=BLOCK_SIZE

# Define some colors (capitals mean these are constants)
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREY     = ( 126, 126, 126)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
YELLOW   = ( 255, 255,   0)
ORANGE   = ( 255, 140,   0)
PURPLE   = ( 139,   0, 139)
CYAN     = (   0, 255, 255)

# initialise pygame
pygame.init()
# open a window
size = (XMAX, YMAX)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris") # title in window bar
score = 0
font = pygame.font.SysFont('Times', 25, True, False)
saved=[] # These will be the stored pieces at the bottom that have stopped moving

# get the blocks to drop
drop = pygame.USEREVENT + 1 # this event is to drop the piece one block
pygame.time.set_timer(drop, 100) # drop every 100 ms

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# check that there is nothing below the piece, if it's clear then drop, if not save
def check_if_clear(piece_coords_x, piece_coords_y,saved):
    if max(piece_coords_y) < 700 - BLOCK_SIZE : # if we're above the bottom
        for _ in range( len(saved) ) : # Almost certainly not the best way to do this
            for ixx in range(4) : # loop over the 4 pieces (one or two are redundant in most pieces, but we won't worry about that now)
                if piece_coords_x[ixx] == saved[_][0] and piece_coords_y[ixx] == saved[_][1] - BLOCK_SIZE :
                    return False
        return True
    else:
        return False


while not done:
# --- Limit to 60 frames per second
    clock.tick(60)



    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        elif event.type == drop: 
            falling_piece.drop_one()

# 1. Fill the screen with black
    screen.fill(BLACK)

# 2. Check if we already have a piece. If not, create one.

    try:
        falling_piece
    except NameError:
        falling_piece=Shape(random.randint(1,7))
    else:
        pass

# 3. Print block
     
    piece_coords_x = [] # will save the piece coordinates so we can check if there's anything below
    piece_coords_y = []

    for x_loop in range( len( falling_piece.piece_matrix ) ):
        for y_loop in range( len( falling_piece.piece_matrix ) ):

            if falling_piece.piece_matrix[y_loop][x_loop] == 1: # why is it this way around??

                piece_coords_x.append(  falling_piece.x + (BLOCK_SIZE * x_loop)  ) # save piece coordinates so
                piece_coords_y.append(  falling_piece.y + (BLOCK_SIZE * y_loop)  ) # we can check below it later

                if falling_piece.y + (BLOCK_SIZE * (y_loop+1)) > UPPER_EDGE :
                    pygame.draw.rect( screen, falling_piece.colour, [ falling_piece.x + (BLOCK_SIZE * x_loop),\
                    falling_piece.y + (BLOCK_SIZE * y_loop) , BLOCK_SIZE, BLOCK_SIZE ] ) # draw piece

# 4. Check if it is clear underneath current block. If not, save block's position, delete, and start a new block

    if check_if_clear( piece_coords_x, piece_coords_y, saved ):
        pass # that's OK
    else: # save block positions, and delete block
        for _ in range(4):
            saved.append( [ piece_coords_x[_], piece_coords_y[_], falling_piece.colour ] )
        del(falling_piece)

# 5. Print the saved blocks (ones that have reached the bottom)
    for block in saved:
        colour = block[2]
        x      = block[0]
        y      = block[1]
        pygame.draw.rect( screen, colour, [ x, y, BLOCK_SIZE, BLOCK_SIZE ] )


















# 1.b draw the game area
    for i in range(11):
        pygame.draw.line(screen, GREY, [50 + BLOCK_SIZE*i , 100], [50 + BLOCK_SIZE*i , 700])
    for i in range(21):
        pygame.draw.line(screen, GREY, [50,100 + BLOCK_SIZE*i], [350,100 + BLOCK_SIZE*i])

# --- Go ahead and update the screen with what we've drawn. Graphics won't be drawn to screen without this
    pygame.display.flip()
 





pygame.quit()