# snake clone

import pygame
import math
import random

# TODO
######## 1. Figuure out how to get the tail to follow - DONE
######## 2. Implement food which grows the snake - DONE
# 3. Conditions for death
# 4. "queue" moves i.e. if I press up then lef in quick succsession, the the snake should first turn up, thenleft on its next move
# 5. high scores

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
WHITE    = ( 255, 255, 255)

# ----- Global variables ------

score=0
high_score=0
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

        self.length = 7
        self.position = []

        for _ in range(self.length):
            self.position.append( [START_POSITION[0] + _ , START_POSITION[1] ] )

        self.vx = speed[0]
        self.vy = speed[1]

        
    def get_direction(self):

        if   self.vx ==  0 and self.vy ==  1 :
            self.direction = 1 # down
        elif self.vx ==  0 and self.vy == -1 :
            self.direction = 2 # up
        elif self.vx == -1 and self.vy ==  0 :
            self.direction = 3 # left
        elif self.vx ==  1 and self.vy ==  0 :
            self.direction = 4 # right


    def move(self):

        x1=self.position[0][0]+self.vx
        y1=self.position[0][1]+self.vy

        self.position.insert( 0 , [ x1 , y1 ] ) # makes the tail follow
        self.position.pop(-1) 

        return [ self.vx , self.vy ]


    def eat(self): # same as move but without removing the final tail
        x1=self.position[0][0]+self.vx
        y1=self.position[0][1]+self.vy

        self.position.insert( 0 , [ x1 , y1 ] )

        self.length += 1

        global score
        score += 1

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


    def check_if_eating(self,x,y):

        if [x,y] in self.position:
            return True
        else:
            return False


class Food:


    def __init__(self):

        self.x = random.randint( 0 , WIDTH - 1 )
        self.y = random.randint( 0 , HEIGHT - 1 )





def to_coords(x1,y1): # write in terms of absolute coordinates (rather than just defined in terms of my board)

    x = x1*BLOCK_SIZE + LEFT_EDGE
    y = y1*BLOCK_SIZE + UPPER_EDGE
    return [x,y]







# ----- Game loop -----

while not done:

# --- Limit to 60 frames per second
    clock.tick(60)
  

# ---- 1. Make the initial snake -----  
    try:
        snake
    except NameError:
        snake=Snake()

# ---- 2. make some food ------

    try:
        food
    except NameError:
        while True:
            food=Food()
            if [ food.x, food.y ] in snake.position :
                del(food)
                food=Food()
            else:
                break


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




# ---- 3. Eat food, grow -----
    if snake.check_if_eating( food.x, food.y ) :
        del(food)
        snake.eat()





# 1. Fill the screen with black
    screen.fill(BLACK)

# 2. Draw the walls
    
    pygame.draw.line(screen, GREEN, [LEFT_EDGE,  LOWER_EDGE], [LEFT_EDGE,  UPPER_EDGE] )
    pygame.draw.line(screen, GREEN, [RIGHT_EDGE, LOWER_EDGE], [RIGHT_EDGE, UPPER_EDGE] )
    pygame.draw.line(screen, GREEN, [LEFT_EDGE,  LOWER_EDGE], [RIGHT_EDGE,  LOWER_EDGE] )
    pygame.draw.line(screen, GREEN, [LEFT_EDGE,  UPPER_EDGE], [RIGHT_EDGE,  UPPER_EDGE] )


# 3. Draw the snake and food

    for _ in range( snake.length ):
        [x,y] = to_coords(snake.position[_][0], snake.position[_][1])
        pygame.draw.rect(screen, GREEN, [x*.88, y*.88, BLOCK_SIZE*.76, BLOCK_SIZE*.76])

    try:
        food_position=to_coords( food.x, food.y )
        pygame.draw.rect(screen, PURPLE, [food_position[0]*.88, food_position[1]*.88 , BLOCK_SIZE*.76, BLOCK_SIZE*.76 ] )
    except NameError:
        pass

# 4. Draw scores
    score_to_print = font.render("SCORE:"+str(score),True,WHITE)
    high_score_to_print = font.render("HIGH SCORE:"+str(high_score),True,WHITE)
    score_width = score_to_print.get_rect().width
    high_score_width = high_score_to_print.get_rect().width
    screen.blit(score_to_print, [ (XMAX/2 - score_width )/2 , BLOCK_SIZE ] )
    screen.blit(high_score_to_print, [ (XMAX/2 - high_score_width )/2 + XMAX/2 , BLOCK_SIZE ] )

    pygame.display.flip()

pygame.quit()







