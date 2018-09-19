import tkinter as tk
import numpy as np


class Player:
    # in common for all players
    playerCount = 0

    def __init__(self):
        Player.playerCount += 1
        if Player.playerCount == 1:
            self.color = 'white'
            self.piece = 1
            self.ai = False
        else:
            self.color = 'black'
            self.piece = -1
            self.ai = False


# Idea: take board as an input so tree nodes can contain parent boards
def update_gui_from_matrix():
    global board
    global root
    for j, row in enumerate(board):
        for i, column in enumerate(row):
            # relief adds an edge to the button so you can see individual squares
            if board[j,i] == 1:
                L = tk.Label(root, text='     ', bg='white', relief='sunken')
                L.grid(row=j, column=i)
            elif board[j, i] == -1:
                L = tk.Label(root, text='     ', bg='black', relief='sunken')
                L.grid(row=j, column=i)


def do_update_gui_and_turn(j, i, event= None):
    global counter
    global curr_p
    board[j][i] = curr_p.piece
    update_gui_from_matrix()
    # Have to change player after update
    counter += 1
    curr_p = p1 if counter % 2 else p2


def make_move(j, i):
    global board
    global curr_p

    if board[j, i] != 0:
        return False

    me = curr_p.piece
    flippable = []

    # Tries to find flips in each direction
    find_flips(me, j, i, 1, 0, flippable)
    find_flips(me, j, i, -1, 0, flippable)
    find_flips(me, j, i, 0, 1, flippable)
    find_flips(me, j, i, 0, -1, flippable)
    find_flips(me, j, i, 1, 1, flippable)
    find_flips(me, j, i, -1, -1, flippable)
    find_flips(me, j, i, 1, -1, flippable)
    find_flips(me, j, i, -1, 1, flippable)

    # checks for an empty list
    if not flippable:
        return False

    # Otherwise flip all flippable
    for fl in flippable:
        board[fl[0],fl[1]] = board[fl[0],fl[1]]*-1
    return True


def find_flips(my_color, y, x, dy, dx, flippable):
    """ Will add any flippable cells to flippable"""
    global board
    new_flip = []
    y += dy
    x += dx
    while 0 <= y <= 7 and 0 <= x <= 7:
        # return if no piece in that direction
        if board[y, x] == 0:
            return
        # When it sees its own piece, mark all opponent's pieces so far as flippable
        if board[y, x] == my_color:
            # extend does nothing if new_flip is empty
            flippable.extend(new_flip)
            return
        # Otherwise it sees an opponents piece
        new_flip.append((y,x))
        y += dy
        x += dx


def on_click(j, i, event):
    valid = make_move(j, i)
    if valid:
        do_update_gui_and_turn(j, i, event)


# Main Program Setup
board = np.zeros((8, 8))
board.astype(dtype=np.int8)  # Note: holds numbers -127 to 128
counter = 1
p1 = Player()
p2 = Player()
curr_p = p1
moves = {}

# Tree node may store any of the following:
# board
# last_move
# score

# Main Program Board/GUI Setup

# Setup of initial 4 squares
board[3, 3] = p1.piece
board[4, 4] = p1.piece
board[3, 4] = p2.piece
board[4, 3] = p2.piece

# Sets up initial GUI. It is an array of buttons.
root = tk.Tk()
for j, row in enumerate(board):
    for i, column in enumerate(row):
        # relief adds an edge to the button so you can see individual squares
        L = tk.Label(root, text='     ',bg='green',relief='sunken')
        L.grid(row=j, column=i)
        # makes GUI change when clicked
        L.bind('<Button-1>',lambda e, j=j, i=i: on_click(j, i, e))

update_gui_from_matrix()

root.mainloop()