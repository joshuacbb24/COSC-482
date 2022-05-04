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
        self.vx = random.uniform(-.03, .03)
        self.vy = random.uniform(-.03, .03)
        self.r = random.uniform(0.1, 0.2)
        self.sides = 50
        self.fill = True
        self.color = [random.random(), random.random(), random.random(), 1]

    def update(self, model, ScreenBounds, time):

        #if elapsed time equals 30 milliseconds execute

        ModelMatrix = glm.mat4(1.0)
        ModelMatrix = glm.translate(ModelMatrix, glm.vec3(self.cx, self.cy, 1))
        #ModelMatrix = glm.scale(ModelMatrix, glm.vec3(0.25, 0.25, 1))
        glUniformMatrix4fv(model, 1, GL_FALSE, glm.value_ptr(ModelMatrix))

        self.cx += self.vx
        self.cy += self.vy

        if self.cx > (ScreenBounds[1] - self.r):
            self.cx = ScreenBounds[1] - self.r
            self.vx = -1 * self.vx

        elif self.cx < (ScreenBounds[0] + self.r):
            self.cx = ScreenBounds[0] + self.r
            self.vx = -1 * self.vx

        if self.cy > (ScreenBounds[3] - self.r):
            self.cy = ScreenBounds[3] - self.r
            self.vy = -1 * self.vy

        elif self.cy < (ScreenBounds[2] + self.r):
            self.cy = ScreenBounds[2] + self.r
            self.vy = -1 * self.vy

    # Set to fill mode.
    def setFill(self):
        self.fill = True

    # Set to outline mode.
    def setOutline(self):
        self.fill = False
