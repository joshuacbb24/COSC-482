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


class Polygon():
    # Constructor
    def __init__(self, ATTS):
        self.atts = ATTS
        #print("atts", self.atts)
        #print("atts x and y", self.atts.cx, self.atts.cx)
        #print("atts color", self.atts.color)
        #print("atts rad", self.atts.r)
        # Setup VAO and buffers.
        self.VAO = glGenVertexArrays(1)
        self.DataBuffer = glGenBuffers(1)
        self.FilledEBO = glGenBuffers(1)
        self.OutlineEBO = glGenBuffers(1)

        self.LoadDataToGraphicsCard()

    # Load vertex, color, and index data to the graphics card.
    def LoadDataToGraphicsCard(self):
        vPosition = 0
        vColor = 1

        # Create vertex and index data.
        vertices = [self.atts.cx, self.atts.cy]
        colors = []
        colors.extend(self.atts.color)

        for i in range(self.atts.sides + 1):
            vertices.extend([self.atts.eyeRadius * np.cos(i*2*np.pi/self.atts.sides) + self.atts.cx,
                             self.atts.eyeRadius * np.sin(i*2*np.pi/self.atts.sides) + self.atts.cy])
            colors.extend(self.atts.color)
        print(vertices)
        print(colors)
        indices = []
        #print("vert", vertices)
        for i in range(self.atts.sides + 2):
            indices.append(i)
        outlineindices = indices[1:]
        # Convert data to GLSL form and get machine sizes of data types.
        indexdata = np.array(indices).astype(ctypes.c_uint)
        outlineindexdata = np.array(outlineindices).astype(ctypes.c_uint)
        vertexdata = np.array(vertices).astype(ctypes.c_float)
        colordata = np.array(colors).astype(ctypes.c_float)
        floatsz = ctypes.sizeof(ctypes.c_float)
        uintsz = ctypes.sizeof(ctypes.c_uint)
        # Bind (turn on) a vertex array.
        glBindVertexArray(self.VAO)
        # Remove old data.

        """
        glDeleteBuffers(1, self.DataBuffer)
        glDeleteBuffers(1, self.FilledEBO)
        glDeleteBuffers(1, self.OutlineEBO)

        # Setup buffers for new data.
        self.DataBuffer = glGenBuffers(1)
        self.FilledEBO = glGenBuffers(1)
        self.OutlineEBO = glGenBuffers(1)
        """
        # Load the indexing array on the graphics card.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.FilledEBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(indices), indexdata, GL_STATIC_DRAW)

        # Load the outline indexing array on the graphics card.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.OutlineEBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(outlineindices), outlineindexdata, GL_STATIC_DRAW)

        # Bindm(turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.DataBuffer)

        # Allocate  space for the vertex and color data.Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(vertices) + len(colors)), None, GL_DYNAMIC_DRAW)

        # Load the vertex data.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(vertices), vertexdata)

        # Load the color data.
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(vertices), floatsz * len(colors), colordata)

        # Setup vertex data position information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vPosition, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

        # Setup color data position information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vColor, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(vertices)))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vColor)

    # Set the center of the box and reload the data.
    def setCenter(self, x, y):
        self.atts.cx = x
        self.atts.cy = y
        self.LoadDataToGraphicsCard()

    # Return the center of the box.
    def getCenter(self):
        return self.atts.cx, self.atts.cy

    # Set the width of the box and reload the data.
    def setRadius(self, rad):
        self.atts.r = rad
        self.LoadDataToGraphicsCard()

    # Return the width of the box.
    def getRadius(self):
        return self.atts.r

    # Set the height of the box and reload the data.
    def setSides(self, s):
        self.atts.sides = s
        self.LoadDataToGraphicsCard()

    # Return the height of the box.
    def getSides(self):
        return self.atts.sides

    # Set to fill mode.
    def setFill(self):
        self.atts.fill = True

    # Set to outline mode.
    def setOutline(self):
        self.atts.fill = False

    # Draw the box.
    def draw(self):
        glBindVertexArray(self.VAO)
        if self.atts.fill:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.FilledEBO)
            glDrawElements(GL_TRIANGLE_FAN, self.atts.sides + 2, GL_UNSIGNED_INT, None)

        else:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.OutlineEBO)
            glDrawElements(GL_LINE_LOOP, self.atts.sides + 1, GL_UNSIGNED_INT, None)
