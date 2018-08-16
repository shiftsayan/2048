####################################
# Imports
####################################

from anytree import Node, RenderTree, LevelOrderGroupIter
import copy

from helper import *

####################################
# Global Variables
####################################

DEPTH = 5
MOVES = [ "Right", "Down", "Left", "Up" ]

MAXIMUMWEIGHT      =  10
SMOOTHNESSWEIGHT   = - 1
MONOTONICITYWEIGHT = -10
EMPTYWEIGHT        =  50

####################################
# Estimator Functions
####################################

def calculate_maximum(board, size):
    '''
    Maximum tile on the board
    '''
    return max(map(max, board)) * MAXIMUMWEIGHT

def calculate_smoothness(board, size):
    '''
    Returns the smoothness of the board (i.e. tiles of the same order should be closer together on the board)
    '''
    smoothness = 0

    for i in range(size):
        for j in range(size):
            for dx, dy in [ (-1, 0), (1, 0), (0, -1), (0, 1) ]:
                if valid_coordinates(i+dx, j+dy, size):
                    if board[i][j] != 0 and board[i+dx][j+dy] != 0:
                        smoothness += abs(board[i][j] - board[i+dx][j+dy])

    return smoothness

def calculate_monotonicity(board, size):
    '''
    Returns monotonicity of the board (i.e. tiles in a row or a column should be increasing or decreasing)
    '''
    monotonicity = 0

    # Horizontal Monotonicity
    for i in range(size):
        temp = [0, 0]
        for sign in [-1, 1]:
            breaks = 0
            for j in range(size-1):
                if board[i][j+1] == 0 or sign * (board[i][j] - board[i][j+1]) <= 0:
                    continue
                else:
                    breaks += 1
            temp[0 if sign == -1 else 1] = breaks
        monotonicity += min(temp)

    # Vertical Monotonicity
    for j in range(size):
        temp = [0, 0]
        for sign in [-1, 1]:
            breaks = 0
            for i in range(size-1):
                if board[i+1][j] == 0 or sign * (board[i][j] - board[i+1][j]) <= 0:
                    continue
                else:
                    breaks += 1
            temp[0 if sign == -1 else 1] = breaks
        monotonicity += min(temp)

    return monotonicity * MONOTONICITYWEIGHT

def calculate_empty(board, size):
    '''
    Returns the number of empty tiles on the board
    '''
    empty = 0

    for i in range(size):
        for j in range(size):
            if board[i][j] == 0: empty += 1

    return empty * EMPTYWEIGHT

def estimator(board, size):
    estimates = [
      calculate_maximum(board, size),
      calculate_smoothness(board, size),
      calculate_monotonicity(board, size),
      calculate_empty(board, size),
    ]
    return sum(estimates)

####################################
# AI Functions
####################################

def generate_game_tree(board, size, target):
    root = Node(0, id="")

    def helper(board, parent, depth):
        if depth == 0:
            return

        for move in MOVES:
            new_board, result, moves = move_sim(copy.deepcopy(board), size, move, target)
            if moves <= 0: continue
            if result not in [ True, False ]: result = estimator(new_board, size)
            child = Node(str(result), parent=parent, id=parent.id + move + ' ')
            helper(new_board, child, depth-1)

    helper(board, root, DEPTH)
    return root

def best_node(nodes):
    best = nodes[0]
    for node in nodes:
        if node.name == "False":
            continue
        elif node.name == "True":
            return node
        elif best.name == "False":
            best = node
        elif int(node.name) > int(best.name):
            best = node
    return best

def ai(board, size, target):
    game_tree = generate_game_tree(board, size, target)
    game_leaf = [ [node for node in children] for children in LevelOrderGroupIter(game_tree) ][-1]
    return best_node(game_leaf).id.split(" ")[0]
