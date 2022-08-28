import numpy as np
import matplotlib.pyplot as plt

pos = np.array([ [1,1], [1,2]])

delta = np.array([[1,0]])
print(pos, delta)
new = np.concatenate((pos, delta), axis =0)
print(new)
dist = np.linalg.norm(pos, axis=1)


ind = np.argwhere(dist<3)

if not np.array([]):
    print('true')

print(pos[ind].reshape(3,2))