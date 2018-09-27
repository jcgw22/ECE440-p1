import numpy as np


x = range(16)
x = np.reshape(x,(4,4))
blank_tiles = np.where(x>9)
ys = blank_tiles[0]
xs = blank_tiles[1]

for i in range(ys.size):
    print (ys[i], ",", xs[i])