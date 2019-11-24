# want to make a program which generates sudokus
# first we could make a filled square

import random
import numpy as np
random.seed(a=1)

n=2
LENGTH=n*n

def split_list( list_input , number_of_sublists ):

    new_list=[]

    n_per_sublist=len(list_input)/number_of_sublists

    ixx = 0

    for i in range(number_of_sublists):
        new_sublist=[]
        for j in range(n_per_sublist):
            new_sublist.append(list_input[ixx])
            ixx += 1 
        new_list.append(new_sublist)

    return new_list



# first make an empty LxL square
empty = [  [0]*LENGTH  for _ in range(LENGTH)]

# next, we'll randomly generate the top left square
initial_square=[ixx for ixx in range(1,1+LENGTH)]
random.shuffle(initial_square) 
for ixx in range(n): # and now we'll put it in
    empty[ixx][0:n]=initial_square[ (ixx*n) : (ixx+1)*n]

def remaining_in_row(sudoku,x,y): # figure out what numbers are left to fill in a row
    remaining=[ixx for ixx in range(1,1+LENGTH)]
    for x_test in sudoku[y] :
        if x_test != 0 :
            remaining.remove(x_test)
    return remaining

def remaining_in_column(sudoku,x,y): # figure out what numbers are left to fill in a column
    remaining=[ixx for ixx in range(1,1+LENGTH)]
    current_column = [sudoku[ixx][x] for ixx in range(LENGTH)] # 
    for y_test in current_column :
        if y_test != 0:
            remaining.remove(y_test)
    return remaining

def remaining_in_square(sudoku,x,y): # figure out what numbers are left to fill in a square




    for x_test in sudoku[y] :
        if x_test != 0 :
            remaining.remove(x_test)
    return remaining

test_list=[[1,2],[3,4]]

remaining_in_column(empty,1,1)

print(empty)

# test_list=[[1,2],[3,4]]
# print(test_list[0])
# print(test_list[1])
# print("")


# print(test_l)

# print(initial_square)
# print(empty)




