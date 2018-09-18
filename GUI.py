import tkinter as tk
import numpy as np


class Player:
    'attributes owned by player'
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


board = np.zeros((8,8))
counter = 0

p1 = Player()
p2 = Player()
curr_p = p1

board[4,4] = p1.piece
board[5,5] = p1.piece
board[4,5] = p2.piece
board[5,4] = p2.piece

event.widget.config(bg=p1.color)


root = tk.Tk()


def on_click(i,j,event):
    global counter
    color = "white" if counter%2 else "black"
    event.widget.config(bg=color)
    board[i][j] = color
    counter += 1
    if counter == 64:
        print('Winner')


for i,row in enumerate(board):
    for j,column in enumerate(row):
        L = tk.Label(root,text='     ',bg='green',relief='sunken')
        L.grid(row=i,column=j)
        L.bind('<Button-1>',lambda e,i=i,j=j: on_click(i,j,e))

root.mainloop()