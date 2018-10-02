import tkinter as tk
import numpy as np


class Player:
    """
    Keeps track of player name, piece count, piece value (1 or -1) and color
    Attributes:
        count of players
    """
    playerCount = 0

    def __init__(self, is_ai):
        Player.playerCount += 1

        if Player.playerCount > 2:
            raise ValueError('Only 2 players can play')

        self.ai = is_ai

        if Player.playerCount == 1:
            self.color = 'white'
            self.int = 1
        else:
            self.color = 'black'
            self.int = -1


class Node(object):
    winning = 0 #p1 white= -1 and p2 black= 1
    alpha =0
    beta =0

    def __init__(self, Board = np.zeros((8, 8), dtype=np.int8), parent=None  ):

        self.children = []
        self.parent = parent
        self.Board = Board

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
    board[3, 3] = p1.int
    board[4, 4] = p1.int
    board[3, 4] = p2.int
    board[4, 3] = p2.int

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
        print_winner()


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
    valid = make_move(j, i, curr_p.int, board)
    if valid:
        # Update GUI and advance ply
        update_gui_and_ply()
        # AI attempts to make a move.
        ai_move()
    else:
        # Finds all moves. If there are no possible moves, the game is over.
        moves = find_moves(curr_p.int, board)
        if moves.size == 0:
            print_winner()


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

    moves = find_moves(curr_p.int, board)
    if moves.size == 0:
        print_winner()
        return

    # Set the move to the first in the list. (Later use minimax here).
    j, i = moves[0][0], moves[0][1]
    make_move(j, i, curr_p.int, board)
    update_gui_and_ply()


def find_moves(player_int, curr_board):
    """
    A move will go [My Piece] [Foe]*(1-6) [Blank] in any of 8 directions.
    The search will start with the player's piece.
    :param player_int: 1 or -1, the two possible piece values
    :param curr_board: the board moves are searched for on
    :return: a nx2 matrix of [[y_values],[x_values]]. If no possible moves, return False
    """

    moves_matrix = np.zeros((8, 8), dtype=np.int8)  # Empty matrix that will hold available move locations

    # Allows to only go through the board for each blank tile
    me_tiles = np.where(curr_board == player_int)  # Which tiles are mine
    ys = me_tiles[0]
    xs = me_tiles[1]

    # For each tile, check each direction for a valid move
    # Needs to check all directions. A matrix is used since could be from multiple directions
    for index in range(ys.size):
            find_moves_dir(ys[index], xs[index], 1, 0, moves_matrix, player_int, curr_board)
            find_moves_dir(ys[index], xs[index], -1, 0, moves_matrix, player_int, curr_board)
            find_moves_dir(ys[index], xs[index], 0, 1, moves_matrix, player_int, curr_board)
            find_moves_dir(ys[index], xs[index], 0, -1, moves_matrix, player_int, curr_board)
            find_moves_dir(ys[index], xs[index], 1, 1, moves_matrix, player_int, curr_board)
            find_moves_dir(ys[index], xs[index], -1, -1, moves_matrix, player_int, curr_board)
            find_moves_dir(ys[index], xs[index], 1, -1, moves_matrix, player_int, curr_board)
            find_moves_dir(ys[index], xs[index], -1, 1, moves_matrix, player_int, curr_board)

    # Change to a format readable by move method.
    moves_temp = np.where(moves_matrix)
    moves = np.column_stack(moves_temp)
    return moves


def find_moves_dir(y, x, dy, dx, moves_matrix, player_int, curr_board):
    """
    Find move going in dy,dx direction from the given y,x position
        assumes given a y,x location belonging to the current player's piece
    :param y: y coordinates of the end piece
    :param x: x coordinate of the end piece
    :param dy: change in y coordinates
    :param dx: change in x coordinates
    :param moves_matrix: will place a 1 in if it is a potential move
    :param player_int: 1 or -1, the two possible piece values
    :param curr_board: the board moves are searched for on
    :return:
    """
    y += dy
    x += dx

    # Makes sure the first piece seen in the opponent's piece
    if not (0 <= y <= 7 and 0 <= x <= 7 and curr_board[y, x] == player_int*-1):
        return
    y += dy
    x += dx

    while 0 <= y <= 7 and 0 <= x <= 7:
        # return if no piece in that direction
        if curr_board[y, x] == player_int:
            return

        # When it sees its own piece, return true as it found it's opponents piece earlier
        if curr_board[y, x] == 0:
            moves_matrix[y, x] = 1
            return

        # The last option is an opponent's piece. Continue.
        y += dy
        x += dx
    return False


def make_move(j, i, player_int, curr_board):
    """
    Attempts to add a piece for the current player in the spot specified.
    This requires that for 1 of 8 possible directions
        1. Current spot is empty
        2. 1-6 concurrent spots contain enemy piece(s)
        3. The next piece belongs to the current player.
    :param j: y position of the placed piece.
    :param i: x position of the placed piece.
    :param player_int: 1 or -1, the two possible piece values
    :param curr_board: the board moves are searched for on
    :return: True if move can be made. False if an invalid move.
    """

    # Checks that the spot selected does not already have a piece.
    # If it does, immediately return false.
    if curr_board[j, i] != 0:
        return False

    flippable = []

    # Tries to find flips in each direction
    make_move_dir(j, i, 1, 0, flippable, player_int, curr_board)
    make_move_dir(j, i, -1, 0, flippable, player_int, curr_board)
    make_move_dir(j, i, 0, 1, flippable, player_int, curr_board)
    make_move_dir(j, i, 0, -1, flippable, player_int, curr_board)
    make_move_dir(j, i, 1, 1, flippable, player_int, curr_board)
    make_move_dir(j, i, -1, -1, flippable, player_int, curr_board)
    make_move_dir(j, i, 1, -1, flippable, player_int, curr_board)
    make_move_dir(j, i, -1, 1, flippable, player_int, curr_board)

    # checks for an empty list
    if not flippable:
        return False

    # Then actually flip the pieces.
    for fl in flippable:
        curr_board[fl[0], fl[1]] = board[fl[0], fl[1]]*-1
    # add the new piece to the board
    curr_board[j][i] = player_int
    return True


def make_move_dir(y, x, dy, dx, flippable, player_int, curr_board):
    """
    Find flippable pieces for the given player, board, and direction
    :param y: y position of proposed move
    :param x: x position of proposed move
    :param dy: y direction checked
    :param dx: x direction checked
    :param flippable: list of potential moves
    :param player_int: int value of current player
    :param curr_board: current board to check for available mores
    :return: 
    """
    new_flip = []
    y += dy
    x += dx
    while 0 <= y <= 7 and 0 <= x <= 7:
        # return if no piece in that direction
        if curr_board[y, x] == 0:
            return
        # When it sees its own piece, mark all opponent's pieces so far as flippable
        if curr_board[y, x] == player_int:
            # extend does nothing if new_flip is empty
            flippable.extend(new_flip)
            return
        # Otherwise it sees an opponents piece. Add to list
        new_flip.append((y, x))
        y += dy
        x += dx


def find_winner(curr_board):
    """
    Compares piece count for both players.
    Return: -1 if Black Won, 0 if Tie, 1 if white won
    """

    result = sum(curr_board)
    if result<1:
        return -1
    if result >1:
        return 1
    return 0


def print_winner():
    """
    Compares piece count for both players.
    Prints result.
    """

    p1_score = np.count_nonzero(board == 1)
    p2_score = 64 - (pieces_left + p1_score)

    if p1_score > p2_score:
        print("White won: ", p1_score, " to ", p2_score)
    elif p2_score > p1_score:
        print("Black won: ", p2_score, " to ", p1_score)
    else:
        print("It was a tie: ",  p2_score, " to ", p1_score)


def min_alpha_beta(board,alpha,beta,level,depth):
    if level == depth:
        return Static_evaluation_function(board)



def max_alpha_beta(board,alpha,beta,level,depth):
    if level == depth:
        return Static_evaluation_function(board)


def Static_evaluation_function(board):
    """
    static evaluation function
    """


# Main Program Setup
board = np.zeros((8, 8), dtype=np.int8)  # Note: holds numbers -127 to 128
pieces_left = 60
p1 = Player(False)
p2 = Player(True)

curr_p = p1

# Main Program Board/GUI Setup
root = tk.Tk()
initial_board_setup()
root.mainloop()
