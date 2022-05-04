#! /usr/bin/env python3
#
# Graphics engine object sets up graphics card programs and data.
# Updates the display and has methods for mode changes and screen shots.
#
# Don Spickler
# 11/20/2021

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from Shader import *
import numpy as np
import ctypes
from PIL import Image
import math
import random
from StarAtts import *

#get outer points of star
count = 0
points = random.randint(5, 15)
#points = 5
oRadius = .8
outerPoints = []
innerPoints = []
#origin coordinate.
origin = [0, 0]
data = []

class Star():
    # "Addresses" for OpenGL constructs.
    Buffer = 0
    vPosition = 0
    vColor = 1
    mode = GL_FILL
    shaderProgram = -1
    oRadius = 0.8

    # Constructor
    def __init__(self, ATTS):
        # Load shaders and compile shader programs.
        self.atts = ATTS
        self.VAO = glGenVertexArrays(1)
        self.DataBuffer = glGenBuffers(1)
        self.FilledEBO = glGenBuffers(1)
        self.OutlineEBO = glGenBuffers(1)
        self.data = []
        self.Vertices = []
        self.indices = []
        self.loadStarData()

    def loadStarData(self):

        oPoints = []
        iPoints = []
        counter = 0
        numpoints = random.randint(5, 15)
        self.data = [self.atts.cx, self.atts.cy]
        self.Vertices = [self.atts.cx, self.atts.cy]
        colors = []
        colors.extend(self.atts.colorCenter)
        for newpoint in range(numpoints):
            oPoints.append([(self.oRadius * (np.cos(((newpoint * 2 * np.pi) / numpoints) + np.pi / 2))),
                            (self.oRadius * (np.sin(((newpoint * 2 * np.pi) / numpoints) + np.pi / 2)))])
            colors.extend(self.atts.color)
            iPoints.append([(self.oRadius / 3 * np.cos(
                ((newpoint * 2 * np.pi) / numpoints) + ((np.pi / numpoints) + (np.pi / 2)))),
                            (self.oRadius / 3 * np.sin(
                                ((newpoint * 2 * np.pi) / numpoints) + ((np.pi / numpoints) + (np.pi / 2))))])
            self.Vertices.extend([oPoints[newpoint][0], oPoints[newpoint][1]])
            self.Vertices.extend([iPoints[newpoint][0], iPoints[newpoint][1]])
            colors.extend(self.atts.color)

        self.Vertices.extend([oPoints[0][0], oPoints[0][1]])
        #self.Vertices.extend([iPoints[numpoints - 1][0], iPoints[numpoints - 1][1]])

        for i in range(len(self.Vertices)):
            self.indices.append(i)
        outlineindices = self.indices[1:]
        # Data for the two triangles to be displayed. Format is (r, g, b, x, y)
        # for each vertex.
        """
        for newpoint in range(numpoints):
            print(counter)
            self.data.append([self.atts.oColorR, self.atts.oColorG, self.atts.oColorB, oPoints[counter][0], oPoints[counter][1]])
            self.indices.append(counter+1)
            self.data.append([self.atts.oColorR, self.atts.oColorG, self.atts.oColorB, iPoints[counter][0], iPoints[counter][1]])
            self.indices.append(counter + 2)
            self.data.append([self.atts.iColorR, self.atts.iColorG, self.atts.iColorB, 0, 0])
            self.indices.append(counter*0)
            if counter < numpoints - 1:
                self.data.append([self.atts.oColorR, self.atts.oColorG, self.atts.oColorB, oPoints[counter + 1][0], oPoints[counter + 1][1]])
                self.data.append([self.atts.oColorR, self.atts.oColorG, self.atts.oColorB, iPoints[counter][0], iPoints[counter][1]])
                self.data.append([self.atts.iColorR, self.atts.iColorG, self.atts.iColorB, 0, 0])

            else:
                self.data.append([self.atts.oColorR, self.atts.oColorG, self.atts.oColorB, oPoints[0][0], oPoints[0][1]])
                self.data.append([self.atts.oColorR, self.atts.oColorG, self.atts.oColorB, iPoints[counter][0], iPoints[counter][1]])
                self.data.append([self.atts.iColorR, self.atts.iColorG, self.atts.iColorB, 0, 0])

            counter += 1
        """
        indexdata = np.array(self.indices).astype(ctypes.c_uint)
        outlineindexdata = np.array(outlineindices).astype(ctypes.c_uint)
        vertexdata = np.array(self.Vertices).astype(ctypes.c_float)
        colordata = np.array(colors).astype(ctypes.c_float)
        floatsz = ctypes.sizeof(ctypes.c_float)
        uintsz = ctypes.sizeof(ctypes.c_uint)
        # Create the Vertex Array Object and bind.
        glBindVertexArray(self.VAO)

        # Load the indexing array on the graphics card.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.FilledEBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(self.indices), indexdata, GL_STATIC_DRAW)

        # Load the outline indexing array on the graphics card.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.OutlineEBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(outlineindices), outlineindexdata, GL_STATIC_DRAW)

        # Bind(turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.DataBuffer)

        # Allocate  space for the vertex and color data.Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(self.Vertices) + len(colors)), None, GL_DYNAMIC_DRAW)

        # Load the vertex data.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(self.Vertices), vertexdata)

        # Load the color data.
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(self.Vertices), floatsz * len(colors), colordata)

        # Setup vertex data position information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(self.vPosition, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

        # Setup color data position information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(self.vColor, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(self.Vertices)))

        # Enable the arrays and set the "positions" for the shaders.
        glEnableVertexAttribArray(self.vPosition)
        glEnableVertexAttribArray(self.vColor)

    # Turn on shader, clear screen, draw triangles, swap display buffers.
    def update(self):
        glUseProgram(self.shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)
        glDrawArrays(GL_TRIANGLES, 0, len(data))

    # Set mode to fill.
    def setFill(self):
        self.mode = GL_FILL

    # Set mode to line.
    def setLine(self):
        self.mode = GL_LINE

    # Set mode to point.
    def setPoint(self):
        self.mode = GL_POINT

    # Dump screen buffer data to raw pixels and convert to PIL Image object.
    def getScreenImage(self):
        viewport = glGetIntegerv(GL_VIEWPORT)
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(viewport[0], viewport[1], viewport[2], viewport[3], GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (viewport[2], viewport[3]), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        return image

    # Draw the box.
    def draw(self):
        glBindVertexArray(self.VAO)
        if self.atts.fill:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.FilledEBO)
            glDrawElements(GL_TRIANGLE_FAN, len(self.Vertices), GL_UNSIGNED_INT, None)
        else:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.OutlineEBO)
            glDrawElements(GL_LINE_LOOP, len(self.Vertices)-1, GL_UNSIGNED_INT, None)