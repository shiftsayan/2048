####################################
# Imports
####################################

import random

####################################
# Helper Functions
####################################

def rgb2hex(r, g, b):
    '''
    Converts RGB color code to hex for tiles
    '''
    return '#%02x%02x%02x' % (r, g, b)

def random_insert(data):
    '''
    Insert a 2-tile in a random position on board
    '''
    free = []
    for i in range(data.grid):
        for j in range(data.grid):
            if data.board[i][j] == 0:
                free.append((i, j))

    i, j = random.choice(free)
    data.board[i][j] = 1

def get_direction(v):
    '''
    Convert event.keysym to directional coordinates
    '''
    if v == "Left":    return -1,  0
    elif v == "Right": return  1,  0
    elif v == "Up":    return  0, -1
    elif v == "Down":  return  0,  1

def get_range(min, max, dir):
    '''
    Get correct direction of board traversal (opposite to movement)
    '''
    if dir > 0:
        return range(max-1, min-1, -1)
    else:
        return range(min, max, 1)

def valid_coordinates(i, j, size):
    '''
    Simple check if (i, j) are valid coordinates on size * size board
    '''
    return 0 <= i and i < size and 0 <= j and j < size

def result_check(data):
    empty = 0

    for i in range(data.grid):
        for j in range(data.grid):
            if data.board[i][j] == 0:
                empty += 1
            if data.board[i][j] == data.target:
                data.is_won = True

    if empty <= 1:
        data.is_lost = True
