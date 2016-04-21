import numpy as np

a = np.array([[1, 1, 1], [0, 0, 2], [0, 2, 0]])
b = np.array([9, 6, 8])
x = np.linalg.solve(a, b)
print x