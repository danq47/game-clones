# Second attempt at tetris clone
# Tetris clone

# TODO
# 1. Rotate using spacebar - DONE
# 2. Stop when the piece is blocked by lower pieces - DONE
# 3. Clear the line if we have a full line
# 4. Look into scoring
# 5. Drop instantly using K_DOWN
# 6. Show outline of where the piece is due to land
# 7. Implement levels
# 8. Implement a high score system
# 9. End if the top layer isn't clear
# 10. Start with a spacebar
# 11. When rotating, check that we won't rotate INTO other blocks
# 11b. Also need to check that the piece can't rotate out of the board

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

        self.get_piece_coordinates() # get the coordinates of the piece



    def get_piece_coordinates(self): # get the (top left) coordinates of the 4 blocks
        self.x_coords=[]
        self.y_coords=[]

        for x_loop in range( len( self.piece_matrix ) ):
            for y_loop in range( len( self.piece_matrix ) ):

                if self.piece_matrix[y_loop][x_loop] == 1: # why is it this way around??
                    self.x_coords.append(  self.x + (BLOCK_SIZE * x_loop)  ) # save piece coordinates so
                    self.y_coords.append(  self.y + (BLOCK_SIZE * y_loop)  ) # we can check below it later



    def rotate(self):
        self.piece_matrix = zip(*self.piece_matrix) # Take the transpose, but now they are given in tuples, so we will have to map(list, matrix)
        self.piece_matrix = map ( list , self.piece_matrix )[::-1] # turn it back into lists, and then write backwards. This gives the matrix rotated 90degrees anticlockwise
        self.get_piece_coordinates()

    def drop_one(self):
        self.y+=BLOCK_SIZE
        self.get_piece_coordinates()


    def move_right(self): # move piece right
        if max(self.x_coords) < RIGHT_EDGE - BLOCK_SIZE:
            self.x+=BLOCK_SIZE
            self.get_piece_coordinates()

    def move_left(self): # move piece left
        if min(self.x_coords) > LEFT_EDGE:
            self.x-=BLOCK_SIZE
            self.get_piece_coordinates()




# ----- Function definitions -----

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

def check_move_left(piece_coords_x, piece_coords_y,saved): # Check that we have space to move sideways
    for _ in range ( len(saved) ) :
        for ixx in range(4) : 
            if piece_coords_y[ixx] == saved[_][1] and piece_coords_x[ixx] == saved[_][0] + BLOCK_SIZE :
                return False
    return True

def check_move_right(piece_coords_x, piece_coords_y,saved): # Check that we have space to move sideways
    for _ in range ( len(saved) ) :
        for ixx in range(4) : 
            if piece_coords_y[ixx] == saved[_][1] and piece_coords_x[ixx] == saved[_][0] - BLOCK_SIZE :
                return False
    return True

def check_for_lines(stored_blocks): # check if we have any complete lines  
    for row in range(20):
        if sum(stored_blocks[row]) == 10:
            print('test')
        else:
            return 0

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
pygame.time.set_timer(drop, 500) # drop every 100 ms

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()




while not done:
# --- Limit to 60 frames per second
    clock.tick(60)



    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == drop:
            try:
                falling_piece.drop_one()
            except NameError:
                falling_piece=Shape(random.randint(1,7))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_SPACE:
                falling_piece.rotate() 
            elif event.key == pygame.K_RIGHT:
                try:
                    if check_move_right( falling_piece.x_coords, falling_piece.y_coords, saved ):
                        falling_piece.move_right()
                except NameError:
                    pass
            elif event.key == pygame.K_LEFT:
                try:
                    if check_move_left( falling_piece.x_coords, falling_piece.y_coords, saved ):
                        falling_piece.move_left()
                except NameError:
                    pass


# 1. Fill the screen with black
    screen.fill(BLACK)

# 2. Check if we already have a piece. If not, create one.

    try:
        falling_piece
    except NameError:
        falling_piece=Shape(random.randint(1,7))
    else:
        pass

# 3. Print piece

    for _ in range(4):
        if falling_piece.y_coords[_] > UPPER_EDGE - BLOCK_SIZE:
            pygame.draw.rect( screen, falling_piece.colour, [falling_piece.x_coords[_] ,\
            falling_piece.y_coords[_], BLOCK_SIZE, BLOCK_SIZE])


# 4. Check if it is clear under piece
    if check_if_clear( falling_piece.x_coords, falling_piece.y_coords, saved ):
        pass # that's OK
    else: # save block positions, and delete block
        for _ in range(4):
            saved.append( [ falling_piece.x_coords[_], falling_piece.y_coords[_], falling_piece.colour ] )
            # print(stored_blocks)
        del(falling_piece)

# 5. Print the saved blocks (ones that have reached the bottom, or are on top of other blocks)
    for block in saved:
        colour = block[2]
        x      = block[0]
        y      = block[1]
        pygame.draw.rect( screen, colour, [ x, y, BLOCK_SIZE, BLOCK_SIZE ] )



# 6. Check for complete lines

    # check_for_lines(stored_blocks)

    








# 1.b draw the game area
    for i in range(11):
        pygame.draw.line(screen, GREY, [50 + BLOCK_SIZE*i , 100], [50 + BLOCK_SIZE*i , 700])
    for i in range(21):
        pygame.draw.line(screen, GREY, [50,100 + BLOCK_SIZE*i], [350,100 + BLOCK_SIZE*i])
# 1.c Print score
    score_to_print = font.render("SCORE:"+str(score),True,WHITE)
    score_width = score_to_print.get_rect().width
    screen.blit(score_to_print, [ (XMAX/2  - score_width )/2 + XMAX/2, YMAX/2 ] )

# --- Go ahead and update the screen with what we've drawn. Graphics won't be drawn to screen without this
    pygame.display.flip()
 





pygame.quit()