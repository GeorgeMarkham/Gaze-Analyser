import numpy as np
import scipy.linalg as lin
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from math import atan
import cv2

with np.load('calib_data.npz') as data:
    K = np.array(data['mtx'])
    #K = [[ 282.363047,      0.,          166.21515189],[   0.,          280.10715905,  108.05494375],[   0.,            0.,            1.        ]]
    rvecs = np.array(data['rvecs'])
    R = cv2.Rodrigues(rvecs)
    sx = K[0][0]
    sy = K[1][1]
    cx = K[0][2]
    cy = K[1][2]

    T = np.array(data['tvecs'])
    #print('sx: ', sx, '\nsy: ', sy, '\n\ncx: ', cx, '\ncy: ', cy)

    x = 708
    y = 397
    x_ext = ((x-cx)/sx)
    y_ext = ((y-cy)/sy)

    coords = np.array([x_ext, y_ext, 1])
    coords = np.hstack(coords)
    print(coords)

    coords_world = np.linalg.inv(K)*coords

    #print(coords_world)

    l = 1

    x_ext_2 = x_ext + (l*cx)
    y_ext_2 = y_ext + (l*cy)

    K_inv = np.linalg.inv(K)
    out_2 = ((x, y, 1)**T)
    out = K_inv * out_2
    #print(out)
    #print('\n\n\n\n')
    #print(np.linalg.inv(K))
    #print(x_ext_2 , ', ', y_ext_2)
