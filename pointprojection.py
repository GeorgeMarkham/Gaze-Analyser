import numpy as np
import scipy.linalg as lin
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from math import atan

with np.load('calib_data.npz') as data:
    K = np.array(data['mtx'])

    R = np.eye(3)
    t = np.array([[0],[1],[0]])
    P = K.dot(np.hstack((R,t)))

    x = np.array([300,300,1])
    X = np.dot(lin.pinv(P),x)
    X = X / X[3] 
    from mpl_toolkits.mplot3d import Axes3D
    w = 20
    f = plt.figure()
    XX  = X[:]; XX[1] = X[2]; XX[2] = X[1]
    ax = f.gca(projection='3d')
    ax.quiver(0, 0, 1., XX[:3][0], XX[:3][1], XX[:3][2],color='red')
    ax.set_xlim(0,10);ax.set_ylim(0,10);ax.set_zlim(0,10)
    ax.quiver(0., 0., 1., 0, 5., 0.,color='blue')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(str(x[0])+","+str(x[1]))
    ax.set_xlim(-w,w);ax.set_ylim(-w,w);ax.set_zlim(-w,w)

    ax.view_init(elev=29, azim=-30)
    fout = 'test_%s_01.png' % (str(x[0])+str(x[1]))
    plt.show(fout)
    #ax.view_init(elev=29, azim=-60)
    #fout = 'test_%s_02.png' % (str(x[0])+str(x[1]))
    #plt.show()