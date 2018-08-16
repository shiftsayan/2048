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

def random_insert(board, grid):
    '''
    Insert a 2-tile in a random position on board
    '''
    free = []

    for i in range(grid):
        for j in range(grid):
            if board[i][j] == 0:
                free.append((i, j))

    i, j = random.choice(free)
    board[i][j] = 1 if random.random() < 0.9 else 2

    return board

def result_check(board, size, target):
    '''
    Check board and return True, False, int for win, lost, continue respectively
    '''
    empty = 0

    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                empty += 1
            elif board[i][j] == target:
                return True # True === Win

    if empty <= 1:
        return False # False === Lost

    return None # None === Continue

def move_to_end(board, size, i, j, dx, dy):
    '''
    Move tile at board[i][j] by (dx, dy) till it reaches end of board
    '''
    cur = board[i][j]
    moves = 0

    while valid_coordinates(i+dy, j+dx, size):
        if board[i+dy][j+dx] == 0:
            board[i+dy][j+dx] = board[i][j]
            board[i][j] = 0
            i += dy
            j += dx
            moves += 1
        elif board[i+dy][j+dx] == cur:
            board[i+dy][j+dx] = board[i][j]+1
            board[i][j] = 0
            moves += 1
            break
        else:
            break

    return moves

def move_sim(board, size, vector, target):
    '''
    Returns board and associated score for resulting state
    '''
    dx, dy = get_direction(vector) # Convert keysym to (dx, dy)
    moves = 0

    for i in get_range(0, size, dx+dy):
        for j in get_range(0, size, dx+dy):
            if board[i][j] > 0:
                moves += move_to_end(board, size, i, j, dx, dy)

    if moves <= 0:
        return board, None, moves # Invalid Move
    else:
        result = result_check(board, size, target)
        if result in [ False, None ]:
            board = random_insert(board, size)
        if result in [ False ]:
            possible_moves = False
            for i in range(size):
                for j in range(size):
                    for dx, dy in [ (-1, 0), (1, 0), (0, -1), (0, 1) ]:
                        if valid_coordinates(i+dx, j+dy, size):
                            if board[i][j] == board[i+dx][j+dy]: possible_moves = True
            if possible_moves: result = None
        return board, result, moves
