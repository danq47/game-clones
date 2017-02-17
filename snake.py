# snake clone

import pygame
import math
import random

# ----- CONSTANTS -----

BLOCK_SIZE=10 # Size of block squares
HEIGHT=30     # playing grid height (in blocks)
WIDTH=60      # playing grid width (in blocks)
SPEED=200 # 1000 ms per block drop
LEVEL=1 # this will increase speed and also score
XMAX=BLOCK_SIZE*(WIDTH + 4)
YMAX=BLOCK_SIZE*(HEIGHT + 6)
LEFT_EDGE=2*BLOCK_SIZE
RIGHT_EDGE=XMAX - 2*BLOCK_SIZE
UPPER_EDGE=4*BLOCK_SIZE
LOWER_EDGE=YMAX - 2*BLOCK_SIZE
START_POSITION=[ WIDTH/2, HEIGHT/2 ] # (x,y)

# ----- Define some colors -----
BLACK    = (   0,   0,   0)
GREY     = ( 126, 126, 126)
GREEN    = (   0, 255,   0)
PURPLE   = ( 139,   0, 139)

# ----- Global variables ------

score=0
game_over = False
speed=[ -1 , 0 ] # (vx,vy)


# ----- initialise pygame -----
pygame.init()
clock = pygame.time.Clock()
size = (XMAX, YMAX)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SNAKE") # title in window bar
font = pygame.font.SysFont('Times', 25, True, False)
# Loop until the user clicks the close button.
done=False
move = pygame.USEREVENT + 1 # move the snake
pygame.time.set_timer(move, SPEED / LEVEL ) 


class Snake:

    def __init__(self):

        self.x  = START_POSITION[0]
        self.y  = START_POSITION[1]
        self.vx = speed[0]
        self.vy = speed[1]

        self.update_position()
        

    def get_direction(self):

        if   self.vx ==  0 and self.vy ==  1 :
            self.direction = 1 # down
        elif self.vx ==  0 and self.vy == -1 :
            self.direction = 2 # up
        elif self.vx == -1 and self.vy ==  0 :
            self.direction = 3 # left
        elif self.vx ==  1 and self.vy ==  0 :
            self.direction = 4 # right


    def update_position(self):

        self.x_coord = self.x*BLOCK_SIZE + LEFT_EDGE
        self.y_coord = self.y*BLOCK_SIZE + UPPER_EDGE

    def move(self):

        self.x+=self.vx
        self.y+=self.vy
        self.update_position()
        return [self.vx , self.vy]


    def turn_up(self,last_move):

        if last_move[0] != 0 :
            self.vx =  0
            self.vy = -1

    def turn_down(self,last_move):

        if last_move[0] != 0 :
            self.vx =  0
            self.vy =  1

    def turn_right(self,last_move):

        if last_move[1] != 0 :
            self.vx =  1
            self.vy =  0

    def turn_left(self,last_move):

        if last_move[1] != 0 :
            self.vx = -1
            self.vy =  0













# ----- Game loop -----

while not done:

# --- Limit to 60 frames per second
    clock.tick(60)
    
    try:
        snake
    except NameError:
        snake=Snake()

    # if snake.move

    for event in pygame.event.get(): # loop over all user events
        if event.type == pygame.QUIT:
            done = True
        elif event.type == move:
            last_move=snake.move()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_LEFT:
                snake.turn_left(last_move)
            elif event.key == pygame.K_RIGHT:
                snake.turn_right(last_move)
            elif event.key == pygame.K_UP:
                snake.turn_up(last_move)
            elif event.key == pygame.K_DOWN:
                snake.turn_down(last_move)








# 1. Fill the screen with black
    screen.fill(BLACK)

# 2. Draw the walls
    
    pygame.draw.line(screen, GREEN, [LEFT_EDGE,  LOWER_EDGE], [LEFT_EDGE,  UPPER_EDGE] )
    pygame.draw.line(screen, GREEN, [RIGHT_EDGE, LOWER_EDGE], [RIGHT_EDGE, UPPER_EDGE] )
    pygame.draw.line(screen, GREEN, [LEFT_EDGE,  LOWER_EDGE], [RIGHT_EDGE,  LOWER_EDGE] )
    pygame.draw.line(screen, GREEN, [LEFT_EDGE,  UPPER_EDGE], [RIGHT_EDGE,  UPPER_EDGE] )


# 3. Draw the snake


    pygame.draw.rect(screen, GREEN, [snake.x_coord, snake.y_coord, BLOCK_SIZE, BLOCK_SIZE])

    pygame.display.flip()

pygame.quit()







