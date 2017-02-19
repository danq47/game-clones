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




# --- Create an initial game menu ----

class GameMenu:

    def __init__(self, screen, items, functions): # need to let the game menu know what screen we're going to put it on
# It will take as an input the list "items" - which it will display. These could be Start, Quit, Level etc
        self.screen = screen
        self.background_colour=BLACK
        self.items = items
        self.functions = functions


    def run(self):

        clock.tick(60)
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
        snake_speed=[-1,0] # inital speed
        last_move=[-1,0] # what was the last move, needed so we dont move snake 180 degrees
        snake = [] 
        snake_length=5
        for _ in range(snake_length): # define the snake's position
            snake.append( [START_POSITION[0] + _ , START_POSITION[1] ] )
        score=0
        game_over = False
        

        done=False # for main game loop
        move = pygame.USEREVENT + 1 # move the snake
        pygame.time.set_timer(move, SPEED * ( 31**(level-1) ) / (40**(level-1)) ) 


# ---- function definitions ------
        def to_coords(x1,y1): # write in terms of absolute coordinates (rather than just defined in terms of my board)
            x = x1*BLOCK_SIZE + LEFT_EDGE
            y = y1*BLOCK_SIZE + UPPER_EDGE
            return [x,y]

        def move_snake():
            snake_head=snake[0] # the first in the list
            x1 = snake_head[0] + snake_speed[0]
            y1 = snake_head[1] + snake_speed[1]
            snake.pop(-1) # delete the tail
            snake.insert( 0, [x1,y1] ) # add the new head in
            return snake_speed

        def up():
            if last_move[0] != 0:
                return [0,-1]
            else:
                return snake_speed

        def down():
            if last_move[0] != 0:
                return [0,1]
            else: return snake_speed

        def left():
            if last_move[1] != 0:
                return [-1,0]
            else:
                return snake_speed

        def right():
            if last_move[1] != 0:
                return [1,0]
            else:
                return snake_speed




        while not done:

            for event in pygame.event.get(): # loop over all user events
                if event.type == pygame.QUIT: done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: done = True
                if event.type == move : last_move=move_snake()
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_UP:
                        snake_speed=up()
                    elif event.key == pygame.K_DOWN:
                        snake_speed=down()
                    elif event.key == pygame.K_LEFT:
                        snake_speed=left()
                    elif event.key == pygame.K_RIGHT:
                        snake_speed=right()



# fill background
                self.screen.fill(self.background_colour)

# print snake
                for _ in range( snake_length ):
                    [x,y] = to_coords(snake[_][0], snake[_][1])
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




if __name__ == "__main__":

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
        if test == "start_game" :
            new_game=GameScreen(screen)
            new_game.run()
        elif test == "quit_game" : 
            game_running = False
            pygame.quit()





pygame.quit()









