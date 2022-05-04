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
import time
import glm
import pygame

class Attributes():
    # Constructor

    def __init__(self, filled):
        self.cx = 0
        self.cy = 0
        self.icx = 0
        self.icy = 0
        self.vr = random.uniform(-500, 500)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.outerR = random.uniform(0.1, .6)
        self.innerR = random.uniform(0.1, 0.2)
        self.sides = random.randint(5, 15)
        self.fill = filled
        self.color = [random.random(), random.random(), random.random(), 1]
        self.colorCenter = [random.random(), random.random(), random.random(), 1]
        # Get the start time of the program.
        self.start_time = time.time()

    def update(self, model, ScreenBounds):

        #if elapsed time equals 30 milliseconds execute
        # Get time change from the start of the program.

        timeNow = time.time()
        dt = timeNow - self.start_time

        self.icx = self.vx * (dt + self.cx)
        self.icy = self.vy * (dt + self.cy)

        ModelMatrix = glm.mat4(1.0)
        ModelMatrix = glm.translate(ModelMatrix, glm.vec3(self.icx, self.icy, 0))
        ModelMatrix = glm.rotate(ModelMatrix, dt * self.vr * np.pi / 180, glm.vec3(0, 0, 1))
        glUniformMatrix4fv(model, 1, GL_FALSE, glm.value_ptr(ModelMatrix))

        if self.cx > (ScreenBounds[1] + self.outerR):
            return True

        elif self.cx < (ScreenBounds[0] - self.outerR):
            return True

        if self.cy > (ScreenBounds[3] + self.outerR):
            return True

        elif self.cy < (ScreenBounds[2] - self.outerR):
            return True

        return False
