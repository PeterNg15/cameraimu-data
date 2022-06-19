import csv
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy
import math
from scipy.spatial.transform import Rotation as R

def IdentityMat44(): return numpy.matrix(numpy.identity(4), copy=False, dtype='float32')

view_mat = IdentityMat44()

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


def Cube():
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,1.0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()
    glFlush()

def Axis():
    """X AXIS"""
    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0) 
    glVertex3f(-4.0, 0.0, 0.0)
    glVertex3f(4.0, 0.0, 0.0)
    glEnd()
    glFlush()

    """Y AXIS"""
    glBegin(GL_LINES)
    glColor3f(0.0,1.0,0.0)
    glVertex3f(0.0, -4.0, 0.0)
    glVertex3f(0.0, 4.0, 0.0);
    glEnd()
    glFlush()
    
    """Z AXIS"""
    glBegin(GL_LINES)
    glColor3f(0.0,0.0,1.0)
    glVertex3f(0.0, 0.0, -4.0)
    glVertex3f(0.0, 0.0, 4.0);
    glEnd()
    glFlush()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    #glMatrixMode(GL_MODELVIEW)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)
    
    fileName = "VID_20220617_144805"

    run = False
    data_file = open('visualization/data/Z_rotation/' + fileName + 'orientation_mod.csv',  'r')
    data_reader = csv.reader(data_file)
    prevX = 0
    prevY = 0
    prevZ = 0
    for row in data_reader:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        r = R.from_euler('xyz', [float(row[0]),float(row[1]),float(row[2])], degrees=True)
        r_matrix = numpy.array(r.as_matrix())
        r_x = math.atan2(r_matrix[2][1], r_matrix[2][2])
        r_y = math.atan2(-r_matrix[2][0], math.sqrt(pow(r_matrix[2][1], 2) + pow(r_matrix[2][2], 2)))
        r_z = math.atan2(r_matrix[1][0], r_matrix[0][0])
        #Reset rotation
        glRotatef(-r_x, 1, 0, 0)
        glRotatef(-r_y, 0, 1, 0)
        glRotatef(-r_z, 0, 0, 1)
        # glRotatef(1, float(row[0]), float(row[1]), float(row[2]))
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Axis()
        Cube()
        pygame.display.flip()
        pygame.time.wait(33)
    
    data_file.close()


main()