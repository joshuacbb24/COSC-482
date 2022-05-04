#! /usr/bin/env python3
#
# Polygon object
#
# Simple polygon object with OpenGL data loading and drawing interfaces.  The data that
# is being stored is created in two separate arrays, one for vertices and the other for
# color.  These blocks of data are transferred to a single array buffer on the graphics
# card in two separate locations (that is the data is not intermixed) and hence we can
# set up the reading pointers as having tightly packed data. There are also two index arrays,
# one for filled triangles and the other for an outline of the polygon.
#
# Don Spickler
# 12/16/2021

from OpenGL.GL import *
import ctypes
import numpy as np
import random
import glm
import time

class LAttributes():
    # Constructor

    def __init__(self):
        self.vx = random.uniform(-.03, .03)
        self.vy = random.uniform(-.03, .03)
        self.pupilRadius = 5
        self.sides = 50
        self.fill = True
        self.eyeDistance = 1
        self.eyeRadius = .15
        self.color = [1, 1, 1, 1]

        self.cx = -.3
        self.cy = 0

    def update(self, model):

        #if elapsed time equals 30 milliseconds execute
        """
        ModelMatrix = glm.mat4(1.0)
        glUniformMatrix4fv(model, 1, GL_FALSE, glm.value_ptr(ModelMatrix))
        """

    # Set to fill mode.
    def setFill(self):
        self.fill = True

    # Set to outline mode.
    def setOutline(self):
        self.fill = False
