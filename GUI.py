import tkinter as tk
import numpy as np
import datetime as dt


class Player:
    # in common for all players
    playerCount = 0

    def __init__(self, is_ai):
        Player.playerCount += 1
        if is_ai:
            self.ai = True
        else:
            self.ai = False
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
    global counter
    global curr_p
    board[j][i] = curr_p.piece
    update_gui_from_matrix()
    # Have to change player after update
    counter += 1
    curr_p = p1 if counter % 2 else p2


def do_ai_move():
    if not curr_p.ai:
        return
    find_moves()

    # Gets the winner if no moves left
    if not moves_b:
        find_winner()

    j, i = moves_b[0]
    make_move(j, i)
    do_update_gui_and_turn(j, i, event=None)


def find_winner():
    print(board)
    total = board.sum()
    if total > 0:
        print("Player 1 won")
    elif total < 0:
        print("Player 2 won")
    else:
        print("It was a tie")
    exit()


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

    # Do ai move and ignore click position for an ai
    if curr_p.ai:
        do_ai_move()
        return

    valid = make_move(j, i)
    if valid:
        # Do the human players move
        do_update_gui_and_turn(j, i, event)
    else:
        find_moves()
        if not moves_b:
            find_winner()
        else:
            print(moves_b[0])

    if counter > 64:
        find_winner()


def find_moves():
    global moves_b
    global moves_f

    moves_b = []
    moves_f = []

# ignore the datetime. I'm not using the values currently.
    a1 = dt.datetime.now()
    for i in range(10):
        find_moves_blank()
    b1 = dt.datetime.now()
    c1 = b1-a1

#    a2 = dt.datetime.now()
#    for i in range(10):
#        find_moves_me()
#    b2 = dt.datetime.now()
#    c2 = b2-a2
#
#    print(counter, " blank: ", c1, " foe: ", c2, " diff b-f ", c1-c2)


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


# Main Program Setup
board = np.zeros((8, 8), dtype=np.int8)  # Note: holds numbers -127 to 128
counter = 1
p1 = Player(False)
p2 = Player(True)
curr_p = p1
moves_b = []
moves_f = []

# Main Program Board/GUI Setup
root = tk.Tk()
initial_board_setup()
root.mainloop()

