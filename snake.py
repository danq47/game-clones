# snake clone

import pygame
import math
import random

# TODO
######## 1. Figuure out how to get the tail to follow - DONE
######## 2. Implement food which grows the snake - DONE
# 3. Conditions for death
# 4. "queue" moves i.e. if I press up then left in quick succsession, the the snake should first turn up, thenleft on its next move
# 5. high scores
# 6. Also need to fix speed, it's far too fast at the moment

# ----- CONSTANTS -----

BLOCK_SIZE=15 # Size of block squares
HEIGHT=30     # playing grid height (in blocks)
WIDTH=60      # playing grid width (in blocks)
SPEED=500 # 1000 ms per move drop
XMAX=BLOCK_SIZE*(WIDTH + 4)
YMAX=BLOCK_SIZE*(HEIGHT + 6)
LEFT_EDGE=2*BLOCK_SIZE
RIGHT_EDGE=XMAX - 2*BLOCK_SIZE
UPPER_EDGE=4*BLOCK_SIZE
LOWER_EDGE=YMAX - 2*BLOCK_SIZE
START_POSITION=[ WIDTH/2, HEIGHT/2 ] # (x,y)
INITIAL_LENGTH=20

# ----- Define some colors -----
BLACK    = (   0,   0,   0)
GREY     = ( 126, 126, 126)
GREEN    = (   0, 255,   0)
BLUE     = (   0,   0, 255)
PURPLE   = ( 139,   0, 139)
WHITE    = ( 255, 255, 255)

# ----- Global variables ------

score=0
high_score=0
game_over = False
speed=[ -1 , 0 ] # (vx,vy)
level=5 # this will increase speed and also score



# ----- initialise pygame -----
pygame.init()
clock = pygame.time.Clock()
size = (XMAX, YMAX)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SNAKE") # title in window bar
font = pygame.font.SysFont('Times', 25, True, False)



class Snake:


    def __init__(self):

        self.length = INITIAL_LENGTH
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

        global game_over

        x1=self.position[0][0]+self.vx
        y1=self.position[0][1]+self.vy

        self.position.pop(-1) # move the tail first
        if [ x1 , y1 ] in self.position:
            game_over = True
        self.position.insert( 0 , [ x1 , y1 ] ) # move the head


        return [ self.vx , self.vy ]


    def eat(self): # same as move but without removing the final tail
        x1=self.position[0][0]+self.vx
        y1=self.position[0][1]+self.vy

        self.position.insert( 0 , [ x1 , y1 ] )

        self.length += 1

        global score
        score += level

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



# ----- Load screen -------

loading = True

while loading :

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loading = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loading = False
            elif event.key == pygame.K_LEFT:
                level-=1
            elif event.key == pygame.K_RIGHT:
                level+=1

    screen.fill(BLACK)

    level_text  = font.render("level: "+str(level),True,WHITE)
    level_text2 = font.render("PRESS LEFT OR RIGHT TO INCREASE OR DECREASE",True,WHITE)
    load_text=font.render("PRESS SPACEBAR TO BEGIN",True,WHITE)
    load_width = load_text.get_rect().width
    level_text_width=level_text.get_rect().width
    level_text2_width = level_text2.get_rect().width
    screen.blit(level_text, [ (XMAX - level_text_width)/2 , YMAX/2 - 8*BLOCK_SIZE])
    screen.blit(level_text2, [ (XMAX - level_text2_width)/2 , YMAX/2 - 5*BLOCK_SIZE])
    screen.blit(load_text, [ (XMAX - load_width )/2 , YMAX/2 ] )

    pygame.display.flip()


# Loop until the user clicks the close button.
done=False
move = pygame.USEREVENT + 1 # move the snake
pygame.time.set_timer(move, SPEED * ( 31**(level-1) ) / (40**(level-1)) ) 

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
        if event.type == pygame.QUIT: done = True
        if event.type == move and not game_over : last_move=snake.move()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE : done = True


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
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


# 4. ---- Check if dead ------
    # if game_over : 



# 1. Fill the screen with black
    screen.fill(BLACK)


# 2. Draw the snake and food

    for _ in range( snake.length ):
        [x,y] = to_coords(snake.position[_][0], snake.position[_][1])
        if _ == 0 :
            pygame.draw.rect(screen, BLUE, [x, y, BLOCK_SIZE, BLOCK_SIZE])
        else:
            pygame.draw.rect(screen, GREEN, [x, y, BLOCK_SIZE, BLOCK_SIZE])
        pygame.draw.rect(screen, BLACK, [x, y, BLOCK_SIZE, BLOCK_SIZE], 2)



    if game_over : 

        for _ in range( snake.length ):
            [x,y] = to_coords(snake.position[_][0], snake.position[_][1])
            pygame.draw.rect(screen, BLACK, [x-100, y-100, BLOCK_SIZE, BLOCK_SIZE ])
        pygame.time.delay(1000)

        done=True
        # for _ in range(snake.length):
        #     [x,y] = to_coords(snake.position[_][0], snake.position[_][1])
        #     pygame.draw.rect(screen, GREEN, [x, y, BLOCK_SIZE, BLOCK_SIZE])
        #     pygame.draw.rect(screen, BLACK, [x, y, BLOCK_SIZE, BLOCK_SIZE], 2)
        # for ixx in range(3): # flash 3 times if it dies
        #     pygame.time.delay(200)

        #     for _ in range( snake.length ):
        #         [x,y] = to_coords(snake.position[_][0], snake.position[_][1])
        #         pygame.draw.rect(screen, BLACK, [x, y, BLOCK_SIZE, BLOCK_SIZE])
                
        #     pygame.time.delay(200)
        #     for _ in range(snake.length):
        #         [x,y] = to_coords(snake.position[_][0], snake.position[_][1])
        #         pygame.draw.rect(screen, GREEN, [x, y, BLOCK_SIZE, BLOCK_SIZE])
        #         pygame.draw.rect(screen, BLACK, [x, y, BLOCK_SIZE, BLOCK_SIZE], 2)
        # done = True

    try:
        food_position=to_coords( food.x, food.y )
        pygame.draw.rect(screen, PURPLE, [food_position[0], food_position[1] , BLOCK_SIZE, BLOCK_SIZE ] )
        pygame.draw.rect(screen, BLACK, [food_position[0], food_position[1] , BLOCK_SIZE, BLOCK_SIZE ], 2 )
    except NameError:
        pass


# 3. Draw the walls
    
    pygame.draw.line(screen, GREEN, [LEFT_EDGE,  LOWER_EDGE], [LEFT_EDGE,  UPPER_EDGE ] )
    pygame.draw.line(screen, GREEN, [RIGHT_EDGE, LOWER_EDGE], [RIGHT_EDGE, UPPER_EDGE ] )
    pygame.draw.line(screen, GREEN, [LEFT_EDGE,  LOWER_EDGE], [RIGHT_EDGE,  LOWER_EDGE] )
    pygame.draw.line(screen, GREEN, [LEFT_EDGE,  UPPER_EDGE], [RIGHT_EDGE,  UPPER_EDGE] )


# 4. Draw scores
    score_to_print = font.render("SCORE:"+str(score),True,WHITE)
    high_score_to_print = font.render("HIGH SCORE:"+str(high_score),True,WHITE)
    score_width = score_to_print.get_rect().width
    high_score_width = high_score_to_print.get_rect().width
    screen.blit(score_to_print, [ (XMAX/2 - score_width )/2 , BLOCK_SIZE ] )
    screen.blit(high_score_to_print, [ (XMAX/2 - high_score_width )/2 + XMAX/2 , BLOCK_SIZE ] )

    pygame.display.flip()

pygame.quit()







