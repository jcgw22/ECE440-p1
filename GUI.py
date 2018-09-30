import tkinter as tk
import numpy as np


class Player:
    """
    Keeps track of player name, piece count, piece value (1 or -1) and color
    Attributes:
        count of players
    """
    playerCount = 0

    def __init__(self, p_name, is_ai):
        Player.playerCount += 1

        if Player.playerCount > 2:
            raise ValueError('Only 2 players can play')

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
    """
    Sets up initial board / GUI
    This includes adding the four initial pieces
    """
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
    """
    Makes the gui accurately reflect the board matrix
    """
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


def update_gui_and_ply():
    """
    Updates the gui using the update_gui_from_matrix method.
    Decrement the pieces left.
    Change the current player.
    If there are no more pieces left, call the find winner method.
    """
    global pieces_left
    global curr_p
    update_gui_from_matrix()
    # Have to change player after update
    pieces_left -= 1
    curr_p = p2 if pieces_left % 2 else p1
    # Check if game is finished
    if pieces_left == 0:
        find_winner()


def ai_move():
    """
    Exits if current player is not an ai.
    Otherwise, finds all possible moves.
    Picks the first move on the list. This should be changed to a minimax selection.
    Makes the move.
    Updates the gui and ends the turn.
    """
    # Checks if the current player is an ai. If not, exits the method.
    if not curr_p.ai:
        return

    find_moves()
    ys = moves[0]
    xs = moves[1]

    # Gets the winner if no moves are found aka game is over.
    if not len(ys):
        find_winner()
        return

    # Set the move to the first in the list. (Later use minimax here).
    j, i = ys[0],xs[0]
    make_move(j, i)
    update_gui_and_ply()


def find_winner():
    """
    Compares piece count for both players.
    Prints result.
    """
    if p1.piece_count > p2.piece_count:
        print(p1.p_name, " won")
    elif p2.piece_count > p1.piece_count:
        print(p2.p_name, " won")
    else:
        print("It was a tie")
    print(p1.p_name, " ", p1.color, ": ", p1.piece_count)
    print(p2.p_name, " ", p2.color, ": ", p2.piece_count)


def make_move(j, i):
    """
    Attempts to add a piece for the current player in the spot specified.
    This requires that for 1 of 8 possible directions
        1. Current spot is empty
        2. 1-6 concurrent spots contain enemy piece(s)
        3. The next piece belongs to the current player.
    :param j: y position of the placed piece.
    :param i: x position of the placed piece.
    :return: True if move can be made. False if an invalid move.
    """
    global board

    # Checks that the spot selected does not already have a piece.
    # If it does, immediately return false.
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

    # First update piece count.
    # The current player steals a number of pieces aka length of flippable
    # The current player also plays 1 additional piece
    diff = len(flippable)
    if pieces_left % 2:
        p1.piece_count += diff + 1
        p2.piece_count -= diff
    else:
        p2.piece_count += diff + 1
        p1.piece_count -= diff

    # Then actually flip the pieces.
    for fl in flippable:
        board[fl[0], fl[1]] = board[fl[0], fl[1]]*-1
    # add the new piece to the board
    board[j][i] = me
    return True


def find_flips(my_color, y, x, dy, dx, flippable):
    """
    Will add any flippable cells to flippable
    """
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
    """
    Clicking will
    1. Have the ai move if it is the current player.
    2. If the player's turn attempt to place a piece in the spot clicked.
        If valid
            update gui and advance ply (aka the other player is now the current player)
            have ai move if it is now the current player.
        Else
            find all possible moves
            If no moves available
                find winner of game
            Else
                exit method to wait for next click
    """

    # Do ai move and ignore click position for an ai. This doesn't happen if curr player isn't an ai
    ai_move()
    # Do the human player's move if it is allowed.
    # valid is set to true if a move was made
    valid = make_move(j, i)
    if valid:
        # Update GUI and advance ply
        update_gui_and_ply()
        # AI attempts to make a move.
        ai_move()
    else:
        # Finds all moves. If there are no possible moves, the game is over.
        find_moves()
        if not moves:
            find_winner()


def find_moves():
    """
    A move will go [Blank] [Foe]*(1-6) [My Piece] in any of 8 directions.
    It is possible to start searching from either end.
        aka check all blank squares or check all of the current pieces.
    There are two possible methods used depending on a comparison of the
    number of blank (empty) spots and the number of pieces owned by the current player.
    """
    global moves

    # pieces_left = number of blank pieces.
    # want to do the minimum amount of work so in this case check all blanks.
    if pieces_left<curr_p.piece_count:
        find_moves_blank()
        moves = moves_b
    else:
        find_moves_me()
        moves = moves_m


def find_moves_blank():
    global moves_b
    moves_matrix = np.zeros((8, 8), dtype=np.int8)  # Empty matrix that will hold available move locations
    me = curr_p.piece

    # Allows to only go through the board for each blank tile
    blank_tiles = np.where(board == 0)
    ys = blank_tiles[0]
    xs = blank_tiles[1]

    # For each tile, check each direction until it finds a valid move.
    # If 1 valid move, there is no need to keep checking
    for index in range(ys.size):
            find_moves_blank_dir(me, ys[index], xs[index], 1, 0, moves_matrix)
            find_moves_blank_dir(me, ys[index], xs[index], -1, 0, moves_matrix)
            find_moves_blank_dir(me, ys[index], xs[index], 0, 1, moves_matrix)
            find_moves_blank_dir(me, ys[index], xs[index], 0, -1, moves_matrix)
            find_moves_blank_dir(me, ys[index], xs[index], 1, 1, moves_matrix)
            find_moves_blank_dir(me, ys[index], xs[index], -1, -1, moves_matrix)
            find_moves_blank_dir(me, ys[index], xs[index], 1, -1, moves_matrix)
            find_moves_blank_dir(me, ys[index], xs[index], -1, 1, moves_matrix)

    # Change to a format readable by move method.
    moves_b = np.where(moves_matrix)


def find_moves_blank_dir(my_color, j, i, dy, dx, moves_matrix):
    """Tries to find moves in 1 direction if given a blank tile"""
    y = dy + j
    x = dx + i

    # Makes sure the first piece seen in the opponent's piece
    if not (0 <= y <= 7 and 0 <= x <= 7 and board[y, x] == my_color*-1):
        return
    y += dy
    x += dx

    while 0 <= y <= 7 and 0 <= x <= 7:
        # return if no piece in that direction
        if board[y, x] == 0:
            return
        # When it sees its own piece, add spot to matrix
        if board[y, x] == my_color:
            moves_matrix[j][i]=1
            return

        # The last option is an opponent's piece. Continue.
        y += dy
        x += dx


def find_moves_me():
    """
    Finds all possible moves by checking all pieces owned by current player
    """
    global moves_m
    moves_matrix = np.zeros((8, 8), dtype=np.int8)  # Empty matrix that will hold available move locations
    me = curr_p.piece

    # Allows to only go through the board for each blank tile
    me_tiles = np.where(board == me)  # Which tiles are mine
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

    # Change to a format readable by move method.
    moves_m = np.where(moves_matrix)


def find_moves_me_dir(me, y, x, dy, dx, moves_matrix):
    """
    Find move going in dy,dx direction from the given y,x position
        assumes given a y,x location belonging to the current player's piece
    :param me: number -1 or 1 of current player
    :param y: y coordinates of the end piece
    :param x: x coordinate of the end piece
    :param dy: change in y coordinates
    :param dx: change in x coordinates
    :param moves_matrix: will place a 1 in if it is a potential move
    :return:
    """
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
            moves_matrix[y, x] = 1
            return

        # The last option is an opponent's piece. Continue.
        y += dy
        x += dx
    return False


# Main Program Setup
board = np.zeros((8, 8), dtype=np.int8)  # Note: holds numbers -127 to 128
pieces_left = 60
p1 = Player("p1", False)
p2 = Player("p2", True)

curr_p = p1
moves_b = []
moves_m = []
moves = None

# Main Program Board/GUI Setup
root = tk.Tk()
initial_board_setup()
root.mainloop()
