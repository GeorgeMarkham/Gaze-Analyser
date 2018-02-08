import numpy as np
import scipy.linalg as lin
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from math import atan

with np.load('calib_data.npz') as data:
    K = np.array(data['mtx'])
    sx = K[0][0]
    sy = K[1][1]
    cx = K[0][2]
    cy = K[1][2]

    print('sx: ', sx, '\nsy: ', sy, '\n\ncx: ', cx, '\ncy: ', cy)

    x = 200
    y = 200
    x_ext = ((x-cx)/sx)
    y_ext = ((y-cy)/sy)

    print('coords: (', x_ext, ', ', y_ext, ', 1)')
    
    C = np.array([[166.21515189],[108.05494375],[1]])
    coords = np.array([10,10,1])
    x_ext_2 = 10/C

    print(x_ext_2)