import numpy as np
import matplotlib as mpl
mpl.use("Qt5Agg")
import matplotlib.pyplot as plt
import cv2
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib import cm
from scipy import ndimage
import math
import csv
import time
from os import startfile



plt.rcParams['figure.figsize'] = (6,4)
plt.rcParams['figure.dpi'] = 150

from scipy.spatial.transform import Rotation as R

def getAxisVectors(x, y, z):
    r = R.from_euler('xyz', [x,y,z], degrees=True)
    return np.array(r.as_matrix())

def updateOrientation(rotationMatrix):
    global quiver_x
    global quiver_y
    global quiver_z
    
    quiver_x.remove()
    quiver_y.remove()
    quiver_z.remove()
    print(rotationMatrix)
    x = rotationMatrix[0]
    y = rotationMatrix[1]
    z = rotationMatrix[2]
    quiver_x = ax.quiver(0,0,0,x[0],x[1],x[2],color='g')
    quiver_y = ax.quiver(0,0,0,y[0],y[1],y[2],color='r')
    quiver_z = ax.quiver(0,0,0,z[0],z[1],z[2],color='b')

def animate(j):
    #if j % 32 != 0:
       # return
    read_file = open('D:/Research/UMass Computer Vision Lab/Rotation Estimation/cameraimu_data_repo/visualization/data/Z_rotation/VID_20220617_144805orientation_mod.csv', 'r')
    reader = csv.reader(read_file)
    
    orientation = next((x for i, x in enumerate(reader) if i == j), None) #orientation at i'th row
    rotationMatrix = getAxisVectors(x=float(orientation[0]), y=float(orientation[1]),z=float(orientation[2]))
    updateOrientation(rotationMatrix)
    _, curr_frame = cap.read()
    RGB_img = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2RGB)
    Rotated_img = cv2.rotate(RGB_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    im.set_array(Rotated_img)
    
fig = plt.figure()
plt.rcParams["figure.autolayout"] = True
ax = fig.add_subplot(122, projection='3d')
ay = fig.add_subplot(121)

ay.set_xlim([0,1080])
ay.set_ylim([0,1920])

ax.set_xlim3d([-1.5,1.5])
ax.set_ylim3d([-1.5,1.5])
ax.set_zlim3d([-1.5,1.5])

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

"""Initiation orientation"""
quiver_x = ax.quiver(0,0,0,1,0,0,color='g')
quiver_y = ax.quiver(0,0,0,0,1,0,color='r')
quiver_z = ax.quiver(0,0,0,0,0,1,color='b')

"""Animation"""
fileName = 'VID_20220617_144805'
cap = cv2.VideoCapture('D:/Research/UMass Computer Vision Lab/Rotation Estimation/cameraimu_data_repo/visualization/data/Z_rotation/' + fileName + '_mod.mp4')
im = ay.imshow(np.random.randn(1920, 1080))

ani = animation.FuncAnimation(fig, animate, interval=3.33)
fig.tight_layout()
plt.show()

# startfile('D:/Research/UMass Computer Vision Lab/Rotation Estimation/cameraimu_data_repo/visualization/data/Z_rotation/' + fileName + '.mp4')
# ani.save("demo.gif", dpi=150, writer=animation.ImageMagickWriter(fps=30, extra_args=['-loop', '1']))