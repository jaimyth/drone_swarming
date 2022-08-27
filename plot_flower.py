import numpy as np
import matplotlib.pyplot as plt
theta = np.deg2rad(np.linspace(0, 360, 2000))
n = 5
k = 1
z = 0
#k = k1/(1-z*np.cos(2*theta))
m = 3

### STAR / POLYGON ###
def r(theta, n):
    return abs(np.cos(n/2 * theta))

r_3 = r(theta, 3)
r_5 = r(theta, 5)

### SQUARE /
#r = np.sqrt(2 / (1 + np.sqrt(1 - ( (2*k**2-1)*np.sin(2*theta)**2 )/k**4)))


fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

ax.plot(theta, r_3, label=f"n={3}")
ax.plot(theta, r_5, label=f'n={5}')
plt.legend()
plt.show()