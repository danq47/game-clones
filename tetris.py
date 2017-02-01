# Tetris clone

# TODO
# 1. Rotate using spacebar
# 2. Stop when the piece is blocked by lower pieces
# 3. Clear the line if we have a full line
# 4. Look into scoring
# 5. Drop instantly using K_DOWN
# 6. Show outline of where the piece is due to land
# 7. Implement levels
# 8. Implement a high score system

import pygame
import math
import random

XMAX=700
YMAX=750
SPEED=6
BLOCK_SIZE=30 # will try this for now, means the game grid will be 300 wide and 600 tall as we need 20x10 blocks
# The grid will go from [50,100] to [350,700]
# Therefore the blocks will start from [50 + 3*BLOCK_SIZE,100] i.e. 3 blocks into the grid
# The square starts at [50 + 4*BLOCK_SIZE, 100 ]
START=[ 50 + 3*BLOCK_SIZE , 100 ]
RIGHT_EDGE=350
LEFT_EDGE=50 # can softcode these in later but for now it's fine
UPPER_EDGE=100
LOWER_EDGE=700

# make a block class. Each "shape" is made of 4 blocks
class Block:

     def __init__(self,x,y):
        self.x = x
        self.y = y

class Shape:

    def __init__ (self,shape):

# We're going to have 7 different possible shapes, characterised by the variable "shape":
# 1 = square, 2 = line, 3 = S, 4 = Z, 5 = T, 6 = L, 7 = backwards L

        if shape == 1 : # square and line start in middle, all others start unevenly to the right
            self.x = START[0] + BLOCK_SIZE
        else:
            self.x = START[0]
        self.y = START[1]

        if shape == 1 :
            self.colour=RED
            self.b1 = Block( self.x, self.y )
            self.b2 = Block( self.x + BLOCK_SIZE, self.y ) # second block is one along
            self.b3 = Block( self.x, self.y + BLOCK_SIZE )
            self.b4 = Block( self.x + BLOCK_SIZE, self.y + BLOCK_SIZE ) # 4th block is three along
        elif shape == 2:
            self.colour=BLUE
            self.b1 = Block( self.x, self.y )
            self.b2 = Block( self.x + BLOCK_SIZE , self.y )
            self.b3 = Block( self.x + 2*BLOCK_SIZE , self.y )
            self.b4 = Block( self.x + 3*BLOCK_SIZE , self.y )
        elif shape == 3:
            self.colour=GREEN
            self.b1 = Block( self.x + BLOCK_SIZE , self.y )
            self.b2 = Block( self.x + 2*BLOCK_SIZE , self.y )
            self.b3 = Block( self.x , self.y + BLOCK_SIZE )
            self.b4 = Block( self.x + BLOCK_SIZE, self.y + BLOCK_SIZE )
        elif shape == 4:
            self.colour=YELLOW
            self.b1 = Block( self.x , self.y )
            self.b2 = Block( self.x + BLOCK_SIZE , self.y )
            self.b3 = Block( self.x + BLOCK_SIZE, self.y + BLOCK_SIZE )
            self.b4 = Block( self.x + 2*BLOCK_SIZE, self.y + BLOCK_SIZE )
        elif shape == 5:
            self.colour=PURPLE
            self.b1 = Block( self.x , self.y )
            self.b2 = Block( self.x + BLOCK_SIZE , self.y )
            self.b3 = Block( self.x + 2*BLOCK_SIZE, self.y )
            self.b4 = Block( self.x + BLOCK_SIZE, self.y + BLOCK_SIZE )
        elif shape == 6: # should probably put this so it comes out layer by layer, can do this later
            self.colour=ORANGE
            self.b1 = Block( self.x , self.y + BLOCK_SIZE)
            self.b2 = Block( self.x + BLOCK_SIZE , self.y + BLOCK_SIZE)
            self.b3 = Block( self.x + 2*BLOCK_SIZE , self.y + BLOCK_SIZE )
            self.b4 = Block( self.x + 2*BLOCK_SIZE, self.y )
        elif shape == 7:
            self.colour=CYAN
            self.b1 = Block( self.x , self.y + BLOCK_SIZE)
            self.b2 = Block( self.x + BLOCK_SIZE , self.y + BLOCK_SIZE)
            self.b3 = Block( self.x + 2*BLOCK_SIZE , self.y + BLOCK_SIZE )
            self.b4 = Block( self.x , self.y )


        self.shape_x = [] # These contains the top right coordinates of each block in the shape
        self.shape_y = []
        for block in [self.b1, self.b2, self.b3, self.b4] :
            self.shape_x.append( block.x )
            self.shape_y.append( block.y )

    def drop_one(self): # method to drop one layer
        for _ in range(4):
            self.shape_y[_]+=BLOCK_SIZE

    def move_right(self): # move piece right
        if max(self.shape_x) < RIGHT_EDGE - BLOCK_SIZE:
            for _ in range(4):
                self.shape_x[_]+=BLOCK_SIZE

    def move_left(self): # move piece left
        if min(self.shape_x) > LEFT_EDGE:
            for _ in range(4):
                self.shape_x[_]-=BLOCK_SIZE


# initialise pygame
pygame.init()

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


# open a window
size = (XMAX, YMAX)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris") # title in window bar
score = 0
font = pygame.font.SysFont('Times', 25, True, False)
saved=[]


# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
#
# --------- Basic game order -----------
# While not done:
#   For each event (keypress, mouse click, etc.):
#   Use a chain of if statements to run code to handle each event.
#   Run calculations to determine where objects move, what happens when objects collide, etc.
#   Clear the screen
#   Draw everything


while not done:
#     # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_LEFT:
                try: # This is necessary, as it is possible at this stage that a new piece hasn't been instantiated yet
                    falling_piece.move_left()   # this would mean we'd be trying to move a piece that doesn't exist
                except NameError:
                    pass
            elif event.key == pygame.K_RIGHT:
                try:
                    falling_piece.move_right()
                except NameError:
                    pass

# 1. Fill the screen with black
    screen.fill(BLACK)

# 2. Start a block falling. Check to see if a block already exists, and if not, instantiate it

    try:
        falling_piece
    except NameError:
        falling_piece=Shape(random.randint(1,7))
    else:
        pass


# 3. Print the block as it is falling and stop it once it hits the bottom
    if max(falling_piece.shape_y) < 700 - BLOCK_SIZE: 
        falling_piece.drop_one()
        for _ in range(4):
            pygame.draw.rect(screen,falling_piece.colour,[ falling_piece.shape_x[_], falling_piece.shape_y[_], BLOCK_SIZE, BLOCK_SIZE ])
        
    else:
        saved.append([ falling_piece.shape_x, falling_piece.shape_y, falling_piece.colour ]) # Save the blocks that have reached the bottom
        del(falling_piece)

# 4. Print the saved blocks (ones that have reached the bottom)
    for block in saved:
        for _ in range(4):
            colour=block[2]
            x=block[0][_]
            y=block[1][_]
            pygame.draw.rect(screen, colour, [ x, y, BLOCK_SIZE, BLOCK_SIZE ])


# 1.b draw the game area
    for i in range(11):
        pygame.draw.line(screen, GREY, [50 + BLOCK_SIZE*i , 100], [50 + BLOCK_SIZE*i , 700])
    for i in range(21):
        pygame.draw.line(screen, GREY, [50,100 + BLOCK_SIZE*i], [350,100 + BLOCK_SIZE*i])

# 1.c Print score
    score_to_print = font.render("SCORE:"+str(score),True,WHITE)
    score_width = score_to_print.get_rect().width
    screen.blit(score_to_print, [ (XMAX/2  - score_width )/2 + XMAX/2, YMAX/2 ] )

# --------- 2. Game logic -----------




    # --- Go ahead and update the screen with what we've drawn. Graphics won't be drawn to screen without this
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(5)


# After we leave the loop, quit pygame properly
pygame.quit()