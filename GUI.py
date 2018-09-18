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
board[3,3] = p1.piece
board[4,4] = p1.piece
board[3,4] = p2.piece
board[4,3] = p2.piece

# Sets up initial GUI. It is an array of buttons.
root = tk.Tk()
for i, row in enumerate(board):
    for j, column in enumerate(row):
        # relief adds an edge to the button so you can see individual squares
        if (i==3 and j==3) or (i==4 and j==4):
            L = tk.Label(root, text='     ', bg='white', relief='sunken')
        elif (i==3 and j==4) or (i == 4 and j == 3):
            L = tk.Label(root, text='     ', bg='black', relief='sunken')
        else:
            L = tk.Label(root,text='     ',bg='green',relief='sunken')
        L.grid(row=i,column=j)
        # makes GUI change when clicked
        L.bind('<Button-1>',lambda e,i=i,j=j: on_click(i,j,e))
root.mainloop()