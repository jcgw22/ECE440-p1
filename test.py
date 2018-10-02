import numpy as np


x = range(16)
x = np.reshape(x,(4,4))

print(np.sum(x))
a = np.bincount(x)
#print(np.bincount(x))
