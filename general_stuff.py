import numpy as np
n_polygon = 7

segment_angles = np.deg2rad(np.linspace(0, 360, n_polygon))[1:]

print(np.rad2deg(segment_angles))