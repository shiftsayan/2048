####################################
# Imports
####################################

from tkinter import *

from helper import *
from ai import *

####################################
# Draw Functions
####################################

def draw_win(canvas, data):
    # Background
    canvas.create_rectangle(0, 0, data.width, data.height, fill=data.end_bg_color, width=0)
    # Text
    canvas.create_text(data.width/2, data.height/2, text="YOU WON :)", font=("Open Sans", "80", "bold"), fill=data.light_text_color)

def draw_lost(canvas, data):
    # Background
    canvas.create_rectangle(0, 0, data.width, data.height, fill=data.end_bg_color, width=0)
    # Text
    canvas.create_text(data.width/2, data.height/2, text="YOU LOST :(", font=("Open Sans", "80", "bold"), fill=data.light_text_color)

def draw_board(canvas, data):
    # Background
    canvas.create_rectangle(0, 0, data.width, data.height, fill=data.game_bg_color, width=0)
    # Tiles
    for i in range(data.grid):
        for j in range(data.grid):
            # Coordinates
            x1 = data.thick * (j+1) + data.size * j
            y1 = data.thick * (i+1) + data.size * i
            x2 = x1 + data.size
            y2 = y1 + data.size
            # Label
            tile_color = data.tile_color[data.board[i][j]]
            text_color = data.dark_text_color if data.board[i][j] < 3 else data.light_text_color
            text = "" if data.board[i][j] == 0 else str(2 ** data.board[i][j])
            # Draw
            canvas.create_rectangle(x1, y1, x2, y2, fill=tile_color, width=0)
            canvas.create_text((x1+x2)/2, (y1+y2)/2, text=text, font=("Open Sans", "55", "bold"), fill=text_color)

####################################
# Move Function
####################################

def move(data, vector):
    if not (data.is_won or data.is_lost):
        if data.is_ai:
            data.board, result, _ = move_sim(data.board, data.grid, ai(data.board, data.grid, data.target), data.target)
        elif vector in [ "Left", "Right", "Up", "Down" ]:
            data.board, result, _ = move_sim(data.board, data.grid, vector, data.target)

        if result not in [ True, False ]:
            pass
        else:
            data.is_won, data.is_lost = (True, False) if result else (False, True)
            data.timerDelay = 1000

####################################
# Animation Functions
####################################

def init(data):
    # Settings
    data.start_tiles = 2
    data.target = 11 # 2 ** 11 = 2048

    # Board
    data.grid  = 4
    data.board = [ [ 0 for i in range(data.grid) ] for i in range(data.grid) ]

    # Sizes
    data.size  = data.width / 4.5
    data.thick = data.size  / 10

    # Colors
    data.game_bg_color = rgb2hex(187, 173, 161)
    data.end_bg_color  = rgb2hex(241, 196,  15)

    data.dark_text_color  = rgb2hex(118, 110, 101)
    data.light_text_color = rgb2hex(249, 246, 242)

    data.tile_color = [
                        rgb2hex(205, 192, 181), # None
                        rgb2hex(238, 228, 218), #    2
                        rgb2hex(237, 224, 200), #    4
                        rgb2hex(242, 177, 121), #    8
                        rgb2hex(245, 149,  99), #   16
                        rgb2hex(246, 124,  95), #   32
                        rgb2hex(246,  94,  59), #   64
                        rgb2hex(237, 207, 114), #  128
                        rgb2hex(237, 204,  97), #  256
                        rgb2hex(237, 200,  80), #  512
                        rgb2hex(237, 197,  63), # 1024
                        rgb2hex(237, 194,  46)  # 2048
                      ]

    # Win States
    data.is_lost = False
    data.is_won  = False

    # Randomly Insert Two 2-tiles
    for i in range(data.start_tiles):
        data.board = random_insert(data.board, data.grid)

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if not data.is_ai: move(data, event.keysym)

def timerFired(data):
    if data.is_ai: move(data, "")

def redrawAll(canvas, data):
    if data.is_won: draw_win(canvas, data)
    elif data.is_lost: draw_lost(canvas, data)
    else: draw_board(canvas, data)

####################################
# Run Function
# Source: www.cs.cmu.edu/~112
####################################

def run(mode, width=600, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    class Struct(object): pass
    data = Struct()
    data.is_ai  = True if mode[0].upper() == 'S' else False # Simulate
    data.width  = width
    data.height = height
    data.timerDelay = 200 # milliseconds
    root = Tk()
    init(data)

    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()

    root.title("2048")
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)

    root.mainloop()

if __name__ == '__main__':
    mode = raw_input("Play or Simulate: ")
    run(mode)
