import numpy as np


x = range(16)
x = np.reshape(x,(4,4))
blank_tiles = np.where(x>9)

