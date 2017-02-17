# Second attempt at tetris clone

# TODO
##### 0. REDO, softcoding in the dimensions - DONE
##### 1. Rotate using spacebar - DONE
##### 2. Stop when the piece is blocked by lower pieces - DONE
##### 3. Clear the line if we have a full line - DONE
##### 4. Look into scoring - DONE
# 5. Drop instantly using K_DOWN - fast drop
# 6. Show outline of where the piece is due to land
##### 7. Implement levels - doesn't change speed yet - DONE
# 8. Implement a high score system 
# 9. End if the top layer isn't clear
# 10. Start with a spacebar
##### 11. When rotating, check that we won't rotate INTO other blocks - DONE
##### 12. RELATED - also need to check that the piece can't rotate out of the board -DONE
##### 13. Want to be able to move it once when it has stopped to either the left or the right - DONE
# 14. Set up a bonus score for consecutive clears
##### 15. Give extra points for a tetris too (clearing 4 lines at once) - DONE
# 16. Show the next 3(/5?) pieces on the side


import pygame
import math
import random
import numpy as np


# ------ CONSTANTS ------

BLOCK_SIZE=30 # Size of block squares
HEIGHT=20     # playing grid height (in blocks)
WIDTH=10      # playing grid width (in blocks)
INITIAL_SPEED=1000 # 1000 ms per block drop
INITIAL_LEVEL=3 # this will increase speed and also score
XMAX=5*BLOCK_SIZE*WIDTH/2
YMAX=BLOCK_SIZE*HEIGHT + 150
LEFT_EDGE=2*BLOCK_SIZE # left edge of grid
RIGHT_EDGE=LEFT_EDGE + (WIDTH*BLOCK_SIZE) # right edge of grid
UPPER_EDGE=3*BLOCK_SIZE 
LOWER_EDGE=UPPER_EDGE + (HEIGHT*BLOCK_SIZE)
START_POSITION=[ 3, -3 ] # starting position of the top left block of the piece (where we are measuring in Blocks rather than coordinates). First block (i.e. the top left) is at position (0,0)

# Define some colors
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

# ----- Global Variables ------

saved=[[0]*WIDTH for _ in range(HEIGHT)] # This stores which blocks have been saved
score=0 
combo_length = 0 # consecutive pieces clearing lines adds a combo score
queue=[random.randint(1,7) for _ in range(5)] # these are the pieces that are coming up 
total_lines_cleared=0


# ----- initialise pygame -----
pygame.init()
clock = pygame.time.Clock()
size = (XMAX, YMAX)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris") # title in window bar
font = pygame.font.SysFont('Times', 25, True, False)
# Loop until the user clicks the close button.
done=False
level = INITIAL_LEVEL
# get the blocks to drop
drop = pygame.USEREVENT + 1 # this event is to drop the piece one block
pygame.time.set_timer(drop, (INITIAL_SPEED * (2**(level-1)))/(3**(level-1)) ) # set frequency of falling block (I've initially set it to 1 per second)





# define the Shape class - this is the piece that will be falling

class Shape:

    def __init__ (self,shape):

        self.shape = shape
        self.x    = START_POSITION[0] # initialise the piece at the top - this is the top left piece in the 4x4 (or 3x3) square
        self.y    = START_POSITION[1]

# We're going to have 7 different possible shapes, characterised by the variable "shape":
        if shape == 1 : # square
            self.piece_matrix = [ [0,0,0,0], [0,1,1,0], [0,1,1,0], [0,0,0,0] ] # no rotation (or 4x4)
            self.colour       = RED
        elif shape == 2: # line
            self.piece_matrix = [ [0,0,0,0], [0,0,0,0], [1,1,1,1], [0,0,0,0] ] # 4x4 rotation
            self.colour       = BLUE
        elif shape == 3: # Z 
            self.piece_matrix = [ [0,0,0], [1,1,0], [0,1,1] ] # 3x3 rotation 
            self.colour       = GREEN
        elif shape == 4: # S
            self.piece_matrix = [ [0,0,0], [0,1,1], [1,1,0] ] # same for all below
            self.colour       = YELLOW
        elif shape == 5: # T
            self.piece_matrix = [ [0,0,0], [1,1,1], [0,1,0] ]
            self.colour       = PURPLE
        elif shape == 6: # L
            self.piece_matrix = [ [0,0,0], [1,1,1], [1,0,0] ]
            self.colour       = ORANGE
        elif shape == 7: # Backwards L
            self.piece_matrix = [ [0,0,0], [1,1,1], [0,0,1] ]
            self.colour       = CYAN

        self.get_piece_coordinates() # get the coordinates of the piece


    def get_piece_coordinates(self): # get the coordinates of the 4 blocks (in terms of the grid)
        self.x_coords=[]
        self.y_coords=[]

        for x_loop in range( len( self.piece_matrix ) ):
            for y_loop in range( len( self.piece_matrix ) ):
                
                if self.piece_matrix[y_loop][x_loop] == 1:
                    self.x_coords.append( x_loop + self.x )
                    self.y_coords.append( y_loop + self.y )
                  
# ----- Functions to check whether it is OK to move down, left, right ------

    def check_below(self): # check that below is clear
        passed = True

        if max(self.y_coords) >= HEIGHT - 1 : # if any of the pieces are in the bottom row then return false (goes to height-1 because we start at 0 and go to 19)
            passed = False
    
        for _ in range(4): # for each block in the piece
            if self.y_coords[_] >= 0: # don't start checking until piece is on the board
                if max(self.y_coords) < HEIGHT - 1  and saved[ self.y_coords[_] + 1 ][ self.x_coords[_] ] != 0: # if any of the pieces have a saved block under them
                    passed = False

        return passed


    def check_above(self): # check that above is clear
        passed = True
    
        for _ in range(4):
            if self.x_coords[_] < 0 or self.x_coords >= WIDTH : # one of the bits at least is off the board
                passed = False
            elif self.y_coords[_] >= 0 :# don't start checking until piece is on the board
                if self.y_coords[_] <= HEIGHT  and saved[ self.y_coords[_] - 1 ][ self.x_coords[_] ] != 0: # if any of the pieces have a saved block above them
                    passed = False


        return passed


    def check_left(self):
        passed = True

        for _ in range(4):
            if self.x_coords[_] < 0 or self.x_coords[_] >= WIDTH : # one of the blocks at least is off the board
                passed = False
            elif self.x_coords[_] == 0 : # we've reached the left wall, can't go further
                passed = False
            elif self.y_coords[_] >= 0 : # start counting once the pieces are on the board
                if saved[ self.y_coords[_] ][ self.x_coords[_] - 1 ] != 0 : # there is a saved block in the way
                    passed = False

        return passed


    def check_right(self):
        passed = True

        for _ in range(4):
            if self.x_coords[_] < 0 or self.x_coords[_] >= WIDTH : # one of the blocks at least is off the board
                passed = False
            elif self.x_coords[_] == WIDTH - 1 : # we've reached the right wall, can't go further
                passed = False
            elif self.y_coords[_] >= 0 : # start counting once the pieces are on the board
                if saved[ self.y_coords[_] ][ self.x_coords[_] + 1 ] != 0 : # there is a saved block in the way
                    passed = False

        return passed



    def check_current(self): # check our current location - this is for rotations
        passed = True # 0 means the piece is OK, 1 means it's too low (rotated out the bottom), 2 means it's too far left, 3 means it's too far right,4 means it's on another piece


        for _ in range(4):
            if self.y_coords[_] >= HEIGHT : # gone too low
                passed = False
            elif self.x_coords[_] < 0 : # gone too far left
                passed = False
            elif self.x_coords[_] >= WIDTH : # gone too far right
                passed = False
            elif saved[ self.y_coords[_] ][ self.x_coords[_] ] != 0 :
                passed = False

        return passed

# ----- Functions to actually move left,right,down -----

    def drop_one(self,saved_list):
        if self.check_below():
            self.y+=1
            self.get_piece_coordinates()
            return True
        else:
            self.save_piece(saved_list)
            return False

    def move_down(self,forced=False): # move down (only for fixing rotations)
        self.y+=1
        self.get_piece_coordinates()


    def move_right(self,forced=False): # move piece left

        move = False

        if forced == True : 
            move = True
        else:
            if self.check_right() : 
                move = True

        if move :
            self.x+=1
            self.get_piece_coordinates()


    def move_left(self,forced=False): # move piece left

        move = False

        if forced == True : 
            move = True
        else:
            if self.check_left() : 
                move = True

        if move :
            self.x-=1
            self.get_piece_coordinates()



    def move_up(self,forced=False):

        move = False

        if forced == True :
            move = True
        else:
            if self.check_above():
                move = True

        if move :
            self.y-=1
            self.get_piece_coordinates()


# ----- ROTATIONS ------



    def rotate(self):

        passed_first_time = False # check whether our rotation has passed (i.e. is in a valid position) after the first set of wall/floor kicks

        def undo_rotate(self):
            for _ in range(3):
                self.piece_matrix = zip(*self.piece_matrix) # Take the transpose, but now they are given in tuples, so we will have to map(list, matrix)
                self.piece_matrix = map ( list , self.piece_matrix )[::-1] # turn it back into lists, and then write backwards. This gives the matrix rotated 90degrees anticlockwise
                self.get_piece_coordinates()

        self.piece_matrix = zip(*self.piece_matrix) # Take the transpose, but now they are given in tuples, so we will have to map(list, matrix)
        self.piece_matrix = map ( list , self.piece_matrix )[::-1] # turn it back into lists, and then write backwards. This gives the matrix rotated 90degrees anticlockwise
        self.get_piece_coordinates()



        if self.check_current() : # check we haven't rotated out of the board left or right, or onto any saved pieces
            pass

        else:
            self.move_up(True)
            if self.check_current() :
                passed_first_time = True
            else:
                self.move_down(True)
                self.move_left(True)
                if self.check_current() :
                    passed_first_time = True
                else:
                    self.move_right(True)
                    self.move_right(True)
                    if self.check_current() :
                        passed_first_time = True
                    else:
                        self.move_left(True)
                        if self.shape != 2 :
                            undo_rotate(self)


            if self.shape == 2 and passed_first_time == False : # if it's an I and the first set of wall/floor kicks hasn't worked
                for _ in range(2):
                    self.move_up(True) # force a double move up
                if self.check_current() : 
                    pass
                else:
                    for _ in range(2): # double move down and left
                        self.move_down(True)
                        self.move_left(True)
                    if self.check_current() :
                        pass
                    else:
                        for _ in range(4):
                            self.move_right(True)
                        if self.check_current() :
                            pass
                        else:
                            for _ in range(2):
                                self.move_left(True)
                            undo_rotate(self)



# ------ Save the pieces that reach the bottom/another piece ----

    def save_piece(self,saved_list): # if it's not clear below then save the pieces
        for _ in range(4):
            saved_list[self.y_coords[_]][self.x_coords[_]] = self.colour


# ------ Check to see if we have any full lines ------

    def check_for_lines(self): # check if we have any full lines
        lines=[]
        for line_number in range(20):
            if 0 not in saved[line_number]:
                lines.append(line_number)
        return lines # return the line numbers as a list

    def clear_lines(self): # if we have any full lines, this method will delete them

        lines_to_clear=self.check_for_lines()
        score_to_add = { 1:40, 2:100, 3:300, 4:1200 } # score per number of lines cleared
        
        global level, score, total_lines_cleared # we are using the global variables here
        
        if len(lines_to_clear) > 0 :
            current_level = level # calculate the current level for calculating the score
            score += current_level*score_to_add[ len(lines_to_clear) ]  # add score
            total_lines_cleared += len(lines_to_clear) # add to lines
            level = total_lines_cleared/10 + INITIAL_LEVEL # increase level every 10 lines we clear
            pygame.time.set_timer(drop, (INITIAL_SPEED * (2**(level-1)))/(3**(level-1)) ) # if we go up a level, increase speed

            for line in lines_to_clear:
                saved.pop(line) # delete the line
                saved.insert( 0, [0 for _ in range(10) ] ) # insert new line at the top

# ------ Convert from block location to actual coordintes -------
def to_coords(x,y):
    x_out = x*BLOCK_SIZE + LEFT_EDGE
    y_out = y*BLOCK_SIZE + UPPER_EDGE
    return [x_out,y_out]









# ------ GAME LOOP -------






while not done:

# --- Limit to 60 frames per second
    clock.tick(60)



    for event in pygame.event.get(): # loop over all user events
        if event.type == pygame.QUIT:
            done = True
        elif event.type == drop:
            try:
                drop_test=falling_piece.drop_one(saved)
                if not drop_test:
                    del(falling_piece)
            except NameError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_LEFT:
                try:
                    falling_piece.move_left()
                except NameError:
                    pass
            elif event.key == pygame.K_RIGHT:
                try:
                    falling_piece.move_right()
                except NameError:
                    pass
            elif event.key == pygame.K_UP:
                try:
                    falling_piece.rotate()
                except NameError:
                    pass



# --- Check we have a piece, otherwise make one ---
    try:
        falling_piece
    except NameError:
        falling_piece=Shape(random.randint(1,7))
    else:
        pass

# 1. soft drop

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        drop_test=True 
        try:
            drop_test=falling_piece.drop_one(saved)
            score+=1
        except NameError:
            pass 
        if not drop_test:
            del(falling_piece)


# 1. Fill the screen with black
    screen.fill(BLACK)


# 2. Print piece

    for _ in range(4):
        try:
            if falling_piece.y_coords[_] >= 0:
                pygame.draw.rect( screen, falling_piece.colour, [LEFT_EDGE + falling_piece.x_coords[_]*BLOCK_SIZE ,\
                UPPER_EDGE + falling_piece.y_coords[_]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])
        except NameError:
            pass
# 3. Print saved

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if saved[y][x] != 0:
                x_to_print=to_coords(x,y)[0]
                y_to_print=to_coords(x,y)[1]
                pygame.draw.rect( screen, saved[y][x], [ x_to_print, y_to_print, BLOCK_SIZE, BLOCK_SIZE])

# 4. Clear lines

    try:
        falling_piece.clear_lines()
    except NameError:
        pass

# --- draw the game area ---

    for x in [BLOCK_SIZE*ixx + LEFT_EDGE for ixx in xrange(WIDTH+1)]:
        pygame.draw.line(screen, GREY, [ x, LOWER_EDGE], [x, UPPER_EDGE] )

    for y in [BLOCK_SIZE*ixx + UPPER_EDGE for ixx in xrange(HEIGHT+1)]:
        pygame.draw.line(screen, GREY, [ LEFT_EDGE, y], [RIGHT_EDGE, y] )

# --- Print score, lines cleared, level ---
    score_to_print = font.render("SCORE:"+str(score),True,WHITE)
    lines_to_print = font.render("LINES:"+str(total_lines_cleared),True,WHITE)
    level_to_print = font.render("LEVEL:"+str(level),True,WHITE)
    score_width = score_to_print.get_rect().width
    lines_width = lines_to_print.get_rect().width
    level_width = level_to_print.get_rect().width
    box_height = score_to_print.get_rect().height
    maxwidth=max([score_width,lines_width,level_width])
    screen.blit(level_to_print, [ (XMAX/2  - maxwidth )/2 + XMAX/2, 3*YMAX/4 ] )
    screen.blit(lines_to_print, [ (XMAX/2  - maxwidth )/2 + XMAX/2, 3*YMAX/4 + box_height ] )
    screen.blit(score_to_print, [ (XMAX/2  - maxwidth )/2 + XMAX/2, 3*YMAX/4 + 2*box_height ] )

# --- Go ahead and update the screen with what we've drawn. Graphics won't be drawn to screen without this
    pygame.display.flip()




pygame.quit()