# snake clone. Second attempt, am trying to make a menu where we can start, quit, change level, view high scores, change walls, go back to when we die

import math
import random
import sys

import pygame

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
INITIAL_LENGTH=5

# ----- Define some colors -----
BLACK    = (   0,   0,   0)
GREY     = ( 126, 126, 126)
GREEN    = (   0, 255,   0)
BLUE     = (   0,   0, 255)
PURPLE   = ( 139,   0, 139)
WHITE    = ( 255, 255, 255)


# --- initialise pygame ---
pygame.init()
clock = pygame.time.Clock()
size = (XMAX, YMAX)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SNAKE") # title in window bar
font = pygame.font.SysFont('Times', 25, True, False)
level = 5
score=0

class Snake:
    def __init__(self):
        self.length = INITIAL_LENGTH
        self.position = []

        for _ in range(self.length):
            self.position.append( [START_POSITION[0] + _ , START_POSITION[1] ] )

        self.vx = -1
        self.vy = 0

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







# --- Create an initial game menu ----

class GameMenu:

    def __init__(self, screen, items, functions): # need to let the game menu know what screen we're going to put it on
# It will take as an input the list "items" - which it will display. These could be Start, Quit, Level etc
        self.screen = screen
        self.background_colour=BLACK
        self.items = items
        self.functions = functions


    def run(self):

        clock.tick(10)
        done=False

# initially we want to select the first item, although we can use the arrow keys to change that
        selected=0

        while not done:

            global level

            for event in pygame.event.get():
                if event.type == pygame.QUIT: done = True
                
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_DOWN and selected < len(self.items) - 1 : # move down the list
                        selected += 1
                    elif event.key == pygame.K_UP and selected > 0: # move up the list
                        selected -= 1

                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN : 
                        self.functions[self.items[selected]]()
                        if self.functions[self.items[selected]]() == "start game":
                            self.output="start_game"
                            done = True
                        elif self.functions[self.items[selected]]() == "quit game":
                            self.output="quit_game"
                            done = True

                    if selected == 1 :
                        if event.key == pygame.K_LEFT :
                            level -= 1
                        elif event.key == pygame.K_RIGHT:
                            level += 1

# draw screen background
                self.screen.fill(self.background_colour)

# write the menu items
                items_to_print=[] # get the menu items rendered as a font
                item_widths=[]    # get the widths of the items so we can line them up equally
                for ixx in range(len(self.items)) : # loop over items to print
                    if self.items[ixx] == "Level:" :
                        menu_item = self.items[ixx]+str(level)
                    else:
                        menu_item = self.items[ixx]

                    if ixx == selected :
                        tmp = font.render(menu_item,True,BLUE)
                    else:
                        tmp = font.render(menu_item,True,GREEN)
                    items_to_print.append(tmp)
                    item_widths.append(tmp.get_rect().width)

                max_width=max(item_widths)

                ixx = 0 # used to iterate the height of the items
                x=(XMAX - max_width)/2 # x position of the menu items
                for _ in items_to_print:
                    y=  YMAX/2 + ixx*2*BLOCK_SIZE - len(self.items)*BLOCK_SIZE # y position of menu items
                    screen.blit( _ , [ x, y] ) # print the item
                    ixx += 1




                pygame.display.flip()








# ----- Main game ------

class GameScreen:

    def __init__(self, screen):
        self.screen = screen
        self.background_colour=BLACK

    def run(self):

        clock.tick(60)
        done=False
        move = pygame.USEREVENT + 1 # move the snake
        pygame.time.set_timer(move, int(SPEED * ( 0.8**level )) ) 
        while not done :
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
                if event.type == move : last_move=snake.move()
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

# fill background
                self.screen.fill(self.background_colour)

# print snake
                for _ in range( snake.length ):
                    [x,y] = to_coords(snake.position[_][0], snake.position[_][1])
                    if _ == 0 :
                        pygame.draw.rect(screen, BLUE, [x, y, BLOCK_SIZE, BLOCK_SIZE])
                    else:
                        pygame.draw.rect(screen, GREEN, [x, y, BLOCK_SIZE, BLOCK_SIZE])
                    pygame.draw.rect(screen, BLACK, [x, y, BLOCK_SIZE, BLOCK_SIZE], 2)



# print walls
                pygame.draw.line(screen, GREEN, [LEFT_EDGE,  LOWER_EDGE], [LEFT_EDGE,  UPPER_EDGE ] )
                pygame.draw.line(screen, GREEN, [RIGHT_EDGE, LOWER_EDGE], [RIGHT_EDGE, UPPER_EDGE ] )
                pygame.draw.line(screen, GREEN, [LEFT_EDGE,  LOWER_EDGE], [RIGHT_EDGE,  LOWER_EDGE] )
                pygame.draw.line(screen, GREEN, [LEFT_EDGE,  UPPER_EDGE], [RIGHT_EDGE,  UPPER_EDGE] )

                pygame.display.flip()




# if __name__ == "__main__":

game_running = True

def start_game():
    return "start game"
def quit_game():
    return "quit game"

game_functions={ 'Start Game':start_game, 'Quit':quit_game}

while game_running :


    menu=GameMenu( screen, ["Start Game", "Level:","Quit"], game_functions )
    menu.run()
    test=menu.output
    del(menu)
    if test == "start_game" :
        new_game=GameScreen(screen)
        new_game.run()
        del(new_game)
    elif test == "quit_game" : 
        game_running = False
        pygame.quit()





pygame.quit()









