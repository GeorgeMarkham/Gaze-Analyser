import numpy as np
import scipy.linalg as lin
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from math import atan

with np.load('calib_data.npz') as data:
    K = np.array(data['mtx'])
    #dist = np.array(data['dist'])
    #rvecs = np.array(data['rvecs'])
    #tvecs = np.array(data['tvecs'])

    R = np.eye(3)
    t = np.array([[0],[1],[0]])
    P = K.dot(np.hstack((R,t)))

    x = np.array([300,300,1])
    X = np.dot(lin.pinv(P),x)
    XX  = X[:]
    XX[1] = X[2]
    XX[2] = X[1]
    x_coord = XX[:3][0]
    y_coord = XX[:3][1]
    z_coord = XX[:3][2]

    gaze_angle = atan((y_coord/x_coord))

    print("θ = \n", gaze_angle)