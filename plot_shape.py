import numpy as np
import matplotlib.pyplot as plt
theta = np.deg2rad(np.linspace(0, 360, 2000))
n = 5
k = 1
z = 0
#k = k1/(1-z*np.cos(2*theta))
m = 3

### STAR / POLYGON ###
def r(theta, n,m,k):
    return np.cos((2*np.arcsin(k)+np.pi*m)/(2*n)) / (np.cos( (2*np.arcsin(k*np.cos(n*theta))+np.pi*m) /(2*n)))

r_star = r(theta, 5,3,0.8)
r_circle = r(theta, 3, 0, 0)
r_poly = r(theta, 2.5,0,1)

### SQUARE /
#r = np.sqrt(2 / (1 + np.sqrt(1 - ( (2*k**2-1)*np.sin(2*theta)**2 )/k**4)))


print(r)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

ax.plot(theta, r_poly, label=f'(n={2.5}, m={0}, k={1})')
ax.plot(theta, r_circle, label=f'(n={3.0}, m={0}, k={0})')
ax.plot(theta, r_star, label=f'(n={5}, m={3}, k={0.8})')
plt.legend()
plt.show()