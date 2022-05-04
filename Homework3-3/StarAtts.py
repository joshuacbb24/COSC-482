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

class Attributes():
    # Constructor

    def __init__(self):
        self.cx = 0
        self.cy = 0
        self.vx = random.uniform(-.003, .003)
        self.vy = random.uniform(-.003, .003)
        self.outerR = random.uniform(0.1, 0.2)
        self.innerR = random.uniform(0.1, 0.2)
        self.sides = random.randint(5, 15)
        self.fill = True
        self.color = [random.random(), random.random(), random.random(), 1]
        self.colorCenter = [random.random(), random.random(), random.random(), 1]

    def update(self, model, ScreenBounds, time):

        #if elapsed time equals 30 milliseconds execute

        ModelMatrix = glm.mat4(1.0)
        ModelMatrix = glm.translate(ModelMatrix, glm.vec3(self.cx, self.cy, 1))
        #ModelMatrix = glm.scale(ModelMatrix, glm.vec3(0.25, 0.25, 1))
        glUniformMatrix4fv(model, 1, GL_FALSE, glm.value_ptr(ModelMatrix))

        self.cx += self.vx
        self.cy += self.vy
        """
        if self.cx > (ScreenBounds[1] + self.outerR):
            self.cx = ScreenBounds[1] - self.r

        elif self.cx < (ScreenBounds[0] - self.outerR):
            self.cx = ScreenBounds[0] + self.r

        if self.cy > (ScreenBounds[3] + self.outerR):
            self.cy = ScreenBounds[3] - self.r

        elif self.cy < (ScreenBounds[2] - self.outerR):
            self.cy = ScreenBounds[2] + self.r
        """

    # Set to fill mode.
    def setFill(self):
        self.fill = True

    # Set to outline mode.
    def setOutline(self):
        self.fill = False
