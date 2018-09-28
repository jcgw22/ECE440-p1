import tkinter as tk
import numpy as np
import datetime as dt
from typing import Any


class Player:
    # in common for all players
    playerCount = 0

    def __init__(self, p_name, is_ai):
        Player.playerCount += 1
        self.piece_count = 2
        self.ai = is_ai
        self.p_name = p_name

        if Player.playerCount == 1:
            self.color = 'white'
            self.piece = 1
        else:
            self.color = 'black'
            self.piece = -1


class Node(object):
    def __init__(self, parent=None):

        self.children = []
        self.parent = parent

    def add_child(self, obj):
        self.children.append(obj)


def initial_board_setup():
    """ Sets up initial board / GUI """
    for j, row in enumerate(board):
        for i, column in enumerate(row):
            # relief adds an edge to the button so you can see individual squares
            label = tk.Label(root, text='     ', bg='green', relief='sunken')
            label.grid(row=j, column=i)
            # makes GUI change when clicked
            label.bind('<Button-1>', lambda e, j=j, i=i: on_click(j, i, e))

    # Setup of initial 4 central squares
    board[3, 3] = p1.piece
    board[4, 4] = p1.piece
    board[3, 4] = p2.piece
    board[4, 3] = p2.piece

    update_gui_from_matrix()


def update_gui_from_matrix():
    global board
    global root
    for j, row in enumerate(board):
        for i, column in enumerate(row):
            # relief adds an edge to the button so you can see individual squares
            if board[j, i] == 1:
                label = tk.Label(root, text='     ', bg='white', relief='sunken')
                label.grid(row=j, column=i)
            elif board[j, i] == -1:
                label = tk.Label(root, text='     ', bg='black', relief='sunken')
                label.grid(row=j, column=i)


def do_update_gui_and_turn(j, i, event=None):
    global pieces_left
    global curr_p
    board[j][i] = curr_p.piece
    update_gui_from_matrix()
    # Have to change player after update
    pieces_left -= 1
    curr_p = p2 if pieces_left % 2 else p1
    # Check if game is finished
    if pieces_left == 0:
        find_winner()


def do_ai_move():
    if not curr_p.ai:
        return
    find_moves()

    # Gets the winner if no moves left
    if not moves:
        find_winner()
        return

    j, i = moves[0]
    make_move(j, i)
    do_update_gui_and_turn(j, i, event=None)


def find_winner():
    if p1.piece_count > p2.piece_count:
        print(p1.p_name, " won")
    elif p2.piece_count > p1.piece_count:
        print(p2.p_name, " won")
    else:
        print("It was a tie")
    print(p1.p_name, " ", p1.color, ": ", p1.piece_count)
    print(p2.p_name, " ", p2.color, ": ", p2.piece_count)


def make_move(j, i):
    global board

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

    # First update piece count
    diff = len(flippable)

    if pieces_left % 2:
        p1.piece_count += diff + 1
        p2.piece_count -= diff
    else:
        p2.piece_count += diff + 1
        p1.piece_count -= diff

    for fl in flippable:
        board[fl[0], fl[1]] = board[fl[0], fl[1]]*-1
    return True


def find_flips(my_color, y, x, dy, dx, flippable):
    """ Will add any flippable cells to flippable"""
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
        new_flip.append((y, x))
        y += dy
        x += dx


def on_click(j, i, event):
    """This advances the game by 1 turn. It ignores the click position for the ai game"""

    # Do ai move and ignore click position for an ai. This doesn't happen if curr player isn't an ai
    do_ai_move()

    valid = make_move(j, i)
    if valid:
        # Do the human players move
        do_update_gui_and_turn(j, i, event)
        do_ai_move()
    else:
        find_moves()
        if not moves:
            find_winner()


def find_moves():
    global moves_b
    global moves_m
    global moves

    moves_b = []
    moves_m = []

## ignore the datetime. I'm not using the values currently.
#    a1 = dt.datetime.now()
#    for i in range(100):
#        find_moves_blank()
#    b1 = dt.datetime.now()
#    c1 = b1-a1
#
#    a2 = dt.datetime.now()
#    for i in range(100):
#        find_moves_me()
#    b2 = dt.datetime.now()
#    c2 = b2-a2
#
#    print(pieces_left, " B: ", c1, " | ", curr_p.piece_count, " Me: ", c2, " diff b-f ", c1-c2, "B-Me ", pieces_left-curr_p.piece_count)

    find_moves_me()
    moves = moves_m

def find_moves_blank_dir(my_color, y, x, dy, dx):
    """Tries to find moves in 1 direction if given a blank tile"""
    y += dy
    x += dx

    # Makes sure the first piece seen in the opponent's piece
    if not (0 <= y <= 7 and 0 <= x <= 7 and board[y, x] == my_color*-1):
        return False
    y += dy
    x += dx

    while 0 <= y <= 7 and 0 <= x <= 7:
        # return if no piece in that direction
        if board[y, x] == 0:
            return False

        # When it sees its own piece, return true as it found it's opponents piece earlier
        if board[y, x] == my_color:
            return True

        # The last option is an opponent's piece. Continue.
        y += dy
        x += dx
    return False


def find_moves_blank():
    global moves_b
    me = curr_p.piece

    # Allows to only go through the board for each blank tile
    blank_tiles = np.where(board == 0)
    ys = blank_tiles[0]
    xs = blank_tiles[1]

    # For each tile, check each direction until it finds a valid move.
    # If 1 valid move, there is no need to keep checking
    for index in range(ys.size):
            if find_moves_blank_dir(me, ys[index], xs[index], 1, 0):
                moves_b.append((ys[index], xs[index]))
                continue
            if find_moves_blank_dir(me, ys[index], xs[index], -1, 0):
                moves_b.append((ys[index], xs[index]))
                continue
            if find_moves_blank_dir(me, ys[index], xs[index], 0, 1):
                moves_b.append((ys[index], xs[index]))
                continue
            if find_moves_blank_dir(me, ys[index], xs[index], 0, -1):
                moves_b.append((ys[index], xs[index]))
                continue
            if find_moves_blank_dir(me, ys[index], xs[index], 1, 1):
                moves_b.append((ys[index], xs[index]))
                continue
            if find_moves_blank_dir(me, ys[index], xs[index], -1, -1):
                moves_b.append((ys[index], xs[index]))
                continue
            if find_moves_blank_dir(me, ys[index], xs[index], 1, -1):
                moves_b.append((ys[index], xs[index]))
                continue
            if find_moves_blank_dir(me, ys[index], xs[index], -1, 1):
                moves_b.append((ys[index], xs[index]))


def find_moves_me_dir(me, y, x, dy, dx, moves_matrix):
    """Tries to find moves in 1 direction if given a blank tile"""
    y += dy
    x += dx

    # Makes sure the first piece seen in the opponent's piece
    if not (0 <= y <= 7 and 0 <= x <= 7 and board[y, x] == me*-1):
        return
    y += dy
    x += dx

    while 0 <= y <= 7 and 0 <= x <= 7:
        # return if no piece in that direction
        if board[y, x] == me:
            return

        # When it sees its own piece, return true as it found it's opponents piece earlier
        if board[y, x] == 0:
            moves_matrix[y,x] = 1
            return

        # The last option is an opponent's piece. Continue.
        y += dy
        x += dx
    return False


def find_moves_me():
    global moves_m
    moves_matrix = np.zeros((8, 8), dtype=np.int8)  # Note: holds numbers -127 to 128
    me = curr_p.piece

    # Allows to only go through the board for each blank tile
    me_tiles = np.where(board == me)
    ys = me_tiles[0]
    xs = me_tiles[1]

    # For each tile, check each direction for a valid move
    # Needs to check all directions. A matrix is used since could be from multiple directions
    for index in range(ys.size):
            find_moves_me_dir(me, ys[index], xs[index], 1, 0, moves_matrix)
            find_moves_me_dir(me, ys[index], xs[index], -1, 0, moves_matrix)
            find_moves_me_dir(me, ys[index], xs[index], 0, 1, moves_matrix)
            find_moves_me_dir(me, ys[index], xs[index], 0, -1, moves_matrix)
            find_moves_me_dir(me, ys[index], xs[index], 1, 1, moves_matrix)
            find_moves_me_dir(me, ys[index], xs[index], -1, -1, moves_matrix)
            find_moves_me_dir(me, ys[index], xs[index], 1, -1, moves_matrix)
            find_moves_me_dir(me, ys[index], xs[index], -1, 1, moves_matrix)

    moves_temp = np.where(moves_matrix)
    ys = moves_temp[0]
    xs = moves_temp[1]
    for index in range(ys.size):
        moves_m.append((ys[index], xs[index]))

# Main Program Setup
board = np.zeros((8, 8), dtype=np.int8)  # Note: holds numbers -127 to 128
pieces_left = 60
p1 = Player("p1", False)
p2 = Player("p2", True)
curr_p = p1
moves_b = []
moves_m = []
moves = []

# Main Program Board/GUI Setup
root = tk.Tk()
initial_board_setup()
root.mainloop()

