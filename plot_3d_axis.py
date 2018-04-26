import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

figure = plt.figure()
figure.gca(projection='3d').quiver(0,0,1, 5,5,5, color='red')
plt.show()