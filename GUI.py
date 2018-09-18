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


# TODO: change grid
# Changes board, but doesn't change grid currently
def manual_move(i, j, player):
    board[i][j] = player.piece


def on_click(i,j,event):
    global counter
    global curr_p
    curr_p = p1 if counter%2 else p2
    event.widget.config(bg=curr_p.color)
    board[i][j] = curr_p.piece
    counter += 1
    if counter == 64:
        print('Winner')


# Main Program Setup
board = np.zeros((8,8))
counter = 0
p1 = Player()
p2 = Player()
curr_p = p1


# Main Program Board/GUI Setup

# Setup of initial 4 squares
board[4,4] = p1.piece
board[5,5] = p1.piece
board[4,5] = p2.piece
board[5,4] = p2.piece
# manual_move(4,4,p1)
# manual_move(5,5,p1)
# manual_move(4,5,p2)
# manual_move(5,4,p2)

# Sets up initial GUI. It is an array of buttons.
root = tk.Tk()
for i, row in enumerate(board):
    for j, column in enumerate(row):
        # relief adds an edge to the button so you can see individual squares
        L = tk.Label(root,text='     ',bg='green',relief='sunken')
        L.grid(row=i,column=j)
        # makes GUI change when clicked
        L.bind('<Button-1>',lambda e,i=i,j=j: on_click(i,j,e))
root.mainloop()