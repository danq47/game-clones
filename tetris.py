# First example of a pygame script
# Can use this as a template for later games

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
            self.b1 = Block( self.x, self.y )
            self.b2 = Block( self.x + BLOCK_SIZE, self.y ) # second block is one along
            self.b3 = Block( self.x, self.y + BLOCK_SIZE )
            self.b4 = Block( self.x + BLOCK_SIZE, self.y + BLOCK_SIZE ) # 4th block is three along
        elif shape == 2:
            self.b1 = Block( self.x, self.y )
            self.b2 = Block( self.x + BLOCK_SIZE , self.y )
            self.b3 = Block( self.x + 2*BLOCK_SIZE , self.y )
            self.b4 = Block( self.x + 3*BLOCK_SIZE , self.y )
        elif shape == 3:
            self.b1 = Block( self.x + BLOCK_SIZE , self.y )
            self.b2 = Block( self.x + 2*BLOCK_SIZE , self.y )
            self.b3 = Block( self.x , self.y + BLOCK_SIZE )
            self.b4 = Block( self.x + BLOCK_SIZE, self.y + BLOCK_SIZE )
        elif shape == 4:
            self.b1 = Block( self.x , self.y )
            self.b2 = Block( self.x + BLOCK_SIZE , self.y )
            self.b3 = Block( self.x + BLOCK_SIZE, self.y + BLOCK_SIZE )
            self.b4 = Block( self.x + 2*BLOCK_SIZE, self.y + BLOCK_SIZE )
        elif shape == 5:
            self.b1 = Block( self.x , self.y )
            self.b2 = Block( self.x + BLOCK_SIZE , self.y )
            self.b3 = Block( self.x + 2*BLOCK_SIZE, self.y )
            self.b4 = Block( self.x + BLOCK_SIZE, self.y + BLOCK_SIZE )
        elif shape == 6: # should probably put this so it comes out layer by layer, can do this later
            self.b1 = Block( self.x , self.y + BLOCK_SIZE)
            self.b2 = Block( self.x + BLOCK_SIZE , self.y + BLOCK_SIZE)
            self.b3 = Block( self.x + 2*BLOCK_SIZE , self.y + BLOCK_SIZE )
            self.b4 = Block( self.x + 2*BLOCK_SIZE, self.y )
        elif shape == 7:
            self.b1 = Block( self.x , self.y + BLOCK_SIZE)
            self.b2 = Block( self.x + BLOCK_SIZE , self.y + BLOCK_SIZE)
            self.b3 = Block( self.x + 2*BLOCK_SIZE , self.y + BLOCK_SIZE )
            self.b4 = Block( self.x , self.y )


        self.shape_vect = [ self.b1, self.b2, self.b3, self.b4 ]

    def drop(self): # method to drop one layer
        for block in self.shape_vect:
            block.y+=BLOCK_SIZE


# initialise pygame
pygame.init()

# Define some colors (capitals mean these are constants)
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
YELLOW   = ( 255, 255,   0)
GREY     = ( 126, 126, 126)


# open a window
size = (XMAX, YMAX)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris") # title in window bar
score = 0
font = pygame.font.SysFont('Times', 25, True, False)

# Initialise blocks
shape1=Shape(7)

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

# quit if we type ESC key
        elif event.type == pygame.KEYDOWN: # not sure what this bit does yet but it is necessary
# OK KEYDOWN says the event was a key was pressed, whereas KEYUP means a key was released. It must
# set the value of event.key
            if event.key == pygame.K_ESCAPE:
                done = True
 

# ---- 1. Fill screen in black -----
    screen.fill(BLACK)

    for _ in range(4):
        pygame.draw.rect(screen,RED,[ shape1.shape_vect[_].x, shape1.shape_vect[_].y, BLOCK_SIZE, BLOCK_SIZE ])
    shape1.drop()
    # print(s1.shape_vect[0].x)

    # pygame.draw.rect(screen,RED,[ s1.x+1, s1.y+1, BLOCK_SIZE, BLOCK_SIZE ]) # -1 so it fits in the grid outline
    # s1.y += s1.speed_y


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
    clock.tick(1)


# After we leave the loop, quit pygame properly
pygame.quit()