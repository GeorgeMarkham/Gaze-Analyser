import numpy as np
import scipy.linalg as lin
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from math import atan

with np.load('calib_data.npz') as data:
    #K = np.array(data['mtx'])
    K = [[ 282.363047,      0.,          166.21515189],[   0.,          280.10715905,  108.05494375],[   0.,            0.,            1.        ]]
    sx = K[0][0]
    sy = K[1][1]
    cx = K[0][2]
    cy = K[1][2]

    print('sx: ', sx, '\nsy: ', sy, '\n\ncx: ', cx, '\ncy: ', cy)

    x = 10
    y = 10
    x_ext = ((x-cx)/sx)
    y_ext = ((y-cy)/sy)

    coords = np.array([x_ext, y_ext, 1])
    coords = np.hstack(coords)
    print(coords)

    coords_world = np.linalg.inv(K)*coords

    print(coords_world)

    l = 1

    x_ext_2 = x_ext + (l*cx)
    y_ext_2 = y_ext + (l*cy)
    print(x_ext_2 , ', ', y_ext_2)
