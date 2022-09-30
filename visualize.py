"""
PyTeapot module for drawing rotating cube using OpenGL as per
quaternion or yaw, pitch, roll angles received over serial port.
"""

import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import csv
import os
from os import startfile
import cv2
from scipy import ndimage
import sys

useSerial = False # set true for using serial for data transmission, false for wifi
useQuat = False   # set true for using quaternions, false for using y,p,r angles
clock = pygame.time.Clock()

def main(fileName):
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    """Setting location"""
    x = 390
    y = 30
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
    """"""
    video_flags = OPENGL | DOUBLEBUF
    pygame.init()
    screen = pygame.display.set_mode((640, 480), video_flags)
    """FOR CSV"""
    data_file = open(curr_dir + "/data/" + fileName+ '/VID_' + fileName  + "_sync_orientation.csv",  'r')
    data_reader = csv.reader(data_file)
    data_list = list(data_reader)[1:]
    """FOR MOVIE"""
    cap = cv2.VideoCapture(curr_dir + "/data/" + fileName + "/VID_" + fileName + '.mp4')
    _, img = cap.read()
    """"""
    pygame.display.set_caption("IMU orientation visualization")
    resizewin(640, 480)
    init()
    frames = 0
    ticks = pygame.time.get_ticks()


    for i in range(len(data_list)):
        row = data_list[i]
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        if(useQuat):
            [w, nx, ny, nz] = read_data()
        else:
            [yaw, pitch, roll] = [float(row[1]),float(row[0]),float(row[2])]
        if(useQuat):
            draw(w, nx, ny, nz)
        else:
            draw(1, yaw, pitch, roll)
        """MOVIE"""
        exist, img = cap.read()
        if not exist == True:
            break
        resize_img = cv2.resize(img, (640,360), interpolation=cv2.INTER_AREA)
        rotated_img = cv2.rotate(resize_img, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow("Phone recording", rotated_img)
        """"""
        pygame.display.flip()
        clock.tick(30)
        frames += 1
    print("fps: %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks)))
    # pygame.display.quit()
    # pygame.quit()
    # cv2.destroyAllWindows()
    exit


def resizewin(width, height):
    """
    For resizing window
    """
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


def cleanSerialBegin():
    if(useQuat):
        try:
            line = ser.readline().decode('UTF-8').replace('\n', '')
            w = float(line.split('w')[1])
            nx = float(line.split('a')[1])
            ny = float(line.split('b')[1])
            nz = float(line.split('c')[1])
        except Exception:
            pass
    else:
        try:
            line = ser.readline().decode('UTF-8').replace('\n', '')
            yaw = float(line.split('y')[1])
            pitch = float(line.split('p')[1])
            roll = float(line.split('r')[1])
        except Exception:
            pass


def draw(w, nx, ny, nz):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0.0, -7.0)
    drawText((-2.6, 1.8, 2), "PyGame", 18)
    drawText((-2.6, 1.6, 2), "Visualize phone orientation", 16)
    drawText((-2.6, -2, 2), "Press Escape to exit.", 16)

    if(useQuat):
        [yaw, pitch , roll] = quat_to_ypr([w, nx, ny, nz])
        drawText((-2.6, -1.8, 2), "Yaw: %f, Pitch: %f, Roll: %f" %(yaw, pitch, roll), 16)
        glRotatef(2 * math.acos(w) * 180.00/math.pi, -1 * nx, nz, ny)
    else:
        yaw = nx
        pitch = ny
        roll = nz
        drawText((-2.6, -1.8, 2), "Yaw: %f, Pitch: %f, Roll: %f" %(yaw, pitch, roll), 16)
        glRotatef(-roll, 0.00, 0.00, 1.00)
        glRotatef(pitch, 1.00, 0.00, 0.00)
        glRotatef(yaw, 0.00, 1.00, 0.00)

    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.4, 1.0, -0.4)
    glVertex3f(-0.4, 1.0, -0.4)
    glVertex3f(-0.4, 1.0, 0.4)
    glVertex3f(0.4, 1.0, 0.4)

    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(0.4, -1.0, 0.4)
    glVertex3f(-0.4, -1.0, 0.4)
    glVertex3f(-0.4, -1.0, -0.4)
    glVertex3f(0.4, -1.0, -0.4)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.4, 1, 0.4)
    glVertex3f(-0.4, 1, 0.4)
    glVertex3f(-0.4, -1, 0.4)
    glVertex3f(0.4, -1, 0.4)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(0.4, -1.0, -0.4)
    glVertex3f(-0.4, -1.0, -0.4)
    glVertex3f(-0.4, 1.0, -0.4)
    glVertex3f(0.4, 1.0, -0.4)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-0.4, 1.0, 0.4)
    glVertex3f(-0.4, 1.0, -0.4)
    glVertex3f(-0.4, -1.0, -0.4)
    glVertex3f(-0.4, -1.0, 0.4)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(0.4, 1.0, -0.4)
    glVertex3f(0.4, 1.0, 0.4)
    glVertex3f(0.4, -1.0, 0.4)
    glVertex3f(0.4, -1.0, -0.4)
    glEnd()


def drawText(position, textString, size):
    font = pygame.font.SysFont("Courier", size, True)
    textSurface = font.render(textString, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def quat_to_ypr(q):
    yaw   = math.atan2(2.0 * (q[1] * q[2] + q[0] * q[3]), q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3])
    pitch = -math.asin(2.0 * (q[1] * q[3] - q[0] * q[2]))
    roll  = math.atan2(2.0 * (q[0] * q[1] + q[2] * q[3]), q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3])
    pitch *= 180.0 / math.pi
    yaw   *= 180.0 / math.pi
    yaw   -= -0.13  # Declination at Chandrapur, Maharashtra is - 0 degress 13 min
    roll  *= 180.0 / math.pi
    return [yaw, pitch, roll]


if __name__ == '__main__':
    main(fileName="20220713_090357")