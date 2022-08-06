import numpy as np
n_polygon = 4

segment_angles = np.deg2rad(np.linspace(0, 360, n_polygon+1))[1:]

print(segment_angles)