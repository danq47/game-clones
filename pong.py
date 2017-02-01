# First example of a pygame script
# Can use this as a template for later games

import pygame
import math
import random

XMAX=700
YMAX=500
DISTANCE_FROM_WALL=10
RACKET_HEIGHT=100
RACKET_WIDTH=10
SPEED=6

class Ball: # class for the ball

    def __init__(self, x=50, y=50):
        self.x=x
        self.y=y
        self.speed_x=-SPEED
        self.speed_y=-SPEED
        self.width=50
        self.height=50

    def draw(self):
        pygame.draw.rect(screen, GREEN, [self.x,self.y, self.width, self.height])

    def bounce_x(self):
        self.speed_x = -1 * self.speed_x + random.uniform(-1,1)

    def bounce_y(self):
        self.speed_y = -1 * self.speed_y 

    def draw_red(self): # if the ball misses the racket
        pygame.draw.rect(screen, RED, [self.x,self.y, self.width+2, self.height+2])

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0

class Racket:

    def __init__(self,x):
        self.height = RACKET_HEIGHT
        self.width = RACKET_WIDTH
        self.x = x
        self.y = (YMAX - self.height ) / 2 

    def draw(self):
        pygame.draw.rect(screen, GREEN, [self.x,self.y, self.width, self.height])



# initialise pygame
pygame.init()

# Define some colors (capitals mean these are constants)
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)


# open a window
size = (XMAX, YMAX)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong") # title in window bar

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



ball = Ball(200 + 75*random.uniform(0,1),300 + 100*random.uniform(0,1)) # instantiate the ball at a (semi-)random point
racket1 = Racket(DISTANCE_FROM_WALL)
racket2 = Racket(XMAX - DISTANCE_FROM_WALL - RACKET_WIDTH)
score1 = 0
score2 = 0
in_play = True # is the ball still in play or has it been missed
font = pygame.font.SysFont('Times', 25, True, False)


def move_1():
    distance = 7.5
    key = pygame.key.get_pressed()

    if key[pygame.K_UP]:
        if racket2.y > 0:
            racket2.y-=distance
    elif key[pygame.K_DOWN]:
        if racket2.y < YMAX - racket2.height:
            racket2.y+=distance
    
    if key[pygame.K_w]:
        if racket1.y > 0:
            racket1.y-=distance
    elif key[pygame.K_s]:
        if racket1.y < YMAX - racket1.height:
            racket1.y+=distance

while not done:
    # --- Main event loop
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

# --------- 2. Game logic -----------


# 2.a ----- draw the 3 objects -----
    if in_play:
        ball.draw()
    else:
        ball.draw_red()

    racket1.draw()
    racket2.draw()

# 2.b ----- Move the ball -----

    ball.x+=ball.speed_x
    ball.y+=ball.speed_y


# 2.c ------------ move the rackets ------------

    move_1()

# 2.d --- bounce the ball if it touches wall ---

    if in_play:
        if ball.y > YMAX - ball.height or ball.y <= 0 :
            ball.bounce_y()

# 2.e --- bounce ball if it touches racket ---
# LHS racket
        if ball.x <= racket1.width + DISTANCE_FROM_WALL:
            if ball.y > racket1.y - ball.height and ball.y < racket1.y + racket1.height :
                ball.bounce_x()
            else:
                in_play = False
                score2 += 1
                ball.stop()
            

# RHS racket
        if ball.x >= XMAX - DISTANCE_FROM_WALL - ball.width - racket2.width - 2 :
            if ball.y > racket2.y - ball.height and ball.y < racket2.y + racket2.height :
                ball.bounce_x()
            else:
                in_play = False
                score1 += 1
                ball.stop()

# If not in play, wait for any key to start again
    else:
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            ball.x = 200 + 75*random.uniform(0,1)
            ball.y = 300 + 100*random.uniform(0,1)
            ball.speed_x = SPEED + random.uniform(-1.5,1.5)
            ball.speed_y = SPEED + random.uniform(-1.5,1.5)
            in_play = True
            





# 3. --- Write score on screen ---
    text1 = font.render("PLR 1 SCORE:"+str(score1),True,WHITE)
    text2 = font.render("PLR 2 SCORE:"+str(score2),True,WHITE)
    width1 = text1.get_rect().width
    width2 = text2.get_rect().width
    screen.blit(text1, [ (XMAX/2  - width1 )/2 , 0.1*YMAX])
    screen.blit(text2, [ ( XMAX/2 - width2 )/2 + ( XMAX / 2 ), 0.1*YMAX])













# TODO
# 1. keep track of score DONE
# 2. print score to screen DONE
# 3. randomize starting position and direction
# 4. bounce off rackets DONE
# 5. move rackets using keys  DONE





    # --- Go ahead and update the screen with what we've drawn. Graphics won't be drawn to screen without this
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)


# After we leave the loop, quit pygame properly
pygame.quit()