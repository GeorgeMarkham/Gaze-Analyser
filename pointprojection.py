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
    print('sx: ', sx, '\nsy: ', sy, '\n\ncx: ', cx, '\ncy: ', cy)

    x = 10
    y = 10
    x_ext = ((x-cx)/sx)
    y_ext = ((y-cy)/sy)

    coords = np.array([x_ext, y_ext, 1])
    coords = np.hstack(coords)
    print('\n\ncoords: ', coords)

    coords_world = np.linalg.inv(K)*coords

    #print(coords_world)

    Esx = sx
    Esy = sy
    Ecx = x_ext
    Ecy = y_ext

    Eye = np.array([[Esx,0.,Ecx],[0., Esy, Ecy],[0.,0.,1.]])

    print('\n\n\n\n\n', Eye)