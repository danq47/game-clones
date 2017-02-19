# snake clone. Second attempt, am trying to make a menu where we can start, quit, change level, view high scores, change walls, go back to when we die

import pygame
import math
import random
import sys


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


# --- initialise pygame ---
pygame.init()
clock = pygame.time.Clock()
size = (XMAX, YMAX)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SNAKE") # title in window bar
font = pygame.font.SysFont('Times', 25, True, False)



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


            for event in pygame.event.get():
                if event.type == pygame.QUIT: done = True
                
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_DOWN and selected < len(self.items) - 1 : # move down the list
                        selected += 1
                    elif event.key == pygame.K_UP and selected > 0: # move up the list
                        selected -= 1

                    if event.key == pygame.K_SPACE : 
                        self.functions[self.items[selected]]()
                        if self.functions[self.items[selected]]() == "start game":
                            self.output="start_game"
                            done = True
                        elif self.functions[self.items[selected]]() == "quit game":
                            self.output="quit_game"
                            done = True


# draw screen background
                self.screen.fill(self.background_colour)

# write the menu items
                items_to_print=[] # get the menu items rendered as a font
                item_widths=[]    # get the widths of the items so we can line them up equally

                for ixx in range(len(self.items)) : # loop over items to print
                    if ixx == selected :
                        tmp = font.render(self.items[ixx],True,BLUE)
                    else:
                        tmp = font.render(self.items[ixx],True,GREEN)
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

        while not done:

            for event in pygame.event.get(): # loop over all user events
                if event.type == pygame.QUIT: done = True

                self.screen.fill(self.background_colour)

                pygame.draw.line(screen, GREEN, [LEFT_EDGE,  LOWER_EDGE], [LEFT_EDGE,  UPPER_EDGE ] )
                pygame.draw.line(screen, GREEN, [RIGHT_EDGE, LOWER_EDGE], [RIGHT_EDGE, UPPER_EDGE ] )
                pygame.draw.line(screen, GREEN, [LEFT_EDGE,  LOWER_EDGE], [RIGHT_EDGE,  LOWER_EDGE] )
                pygame.draw.line(screen, GREEN, [LEFT_EDGE,  UPPER_EDGE], [RIGHT_EDGE,  UPPER_EDGE] )

                pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":

    def start_game():
        # new_game=GameScreen(screen)
        return "start game"
    def quit_game():
        return "quit game"


    game_functions={ 'Start Game':start_game, 'Quit':quit_game}

    menu=GameMenu( screen, ["Start Game", "Quit"], game_functions )
    menu.run()
    test=menu.output
    if test == "start_game" :
        new_game=GameScreen(screen)
        new_game.run()
    elif test == "quit_game" : 
        pygame.quit()





pygame.quit()









