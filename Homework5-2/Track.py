#! /usr/bin/env python3
#
# Cube object
#
# Simple cube object with OpenGL data loading and drawing interfaces.  The data that
# is being stored is created in two separate arrays, one for vertices and the other for
# color.  These blocks of data are transferred to a single array buffer on the graphics
# card in two separate locations (that is the data is not intermixed) and hence we can
# set up the reading pointers as having tightly packed data. There are also index arrays
# for drawing faces and for outlines.
#
# The cube is centered at the origin and is unit length in all three directions.
#
# Don Spickler
# 12/30/2021

from OpenGL.GL import *
import ctypes
import numpy as np


class Track():
    # Constructor
    indiciesFill = []
    indiciesFill2 = []
    def __init__(self):
        self.drawStyle = 0
        self.LoadDataToGraphicsCard()

    # Load vertex, color, and index data to the graphics card.
    def LoadDataToGraphicsCard(self):
        vPosition = 0
        vColor = 1

        # Vertex data for the cube.
        vertices = []
        colors = []
        colors2 = []
        vertices2 = []
        ties = []

        """
        for i in range(0.0, 2*np.pi, 0.1):
            x = r*np.cos(i)
            y = (np.sin(3*i)) - 2*np.cos(2(i + 0.2)) + (2*np.sin(7*i))
            z = r*np.sin(i)
            vertices.extend([x, y, z])
        
        print("vertices", vertices)
        """
        r = 9.8
        for i in range(500):
            theta = i * ((2*np.pi) / 500)
            x = r*np.cos(theta)
            #print(x)
            y = (np.sin(3*theta)) - 2*np.cos(2*(theta + 0.2)) + (2*np.sin(7*theta))
            #print(y)
            z = r*np.sin(theta)
            #print(z)
            vertices.extend([x, y, z, 1])
            colors.extend([1, 1, 1])
            self.indiciesFill.append(i)

        r = 10.2
        for i in range(500):
            theta = i * ((2*np.pi) / 500)
            x = r*np.cos(theta)
            #print(x)
            y = (np.sin(3*theta)) - 2*np.cos(2*(theta + 0.2)) + (2*np.sin(7*theta))
            #print(y)
            z = r*np.sin(theta)
            #print(z)
            vertices2.extend([x, y, z, 1])

        for i in range(500):
            ties.extend([vertices[4 * i], vertices[4 * i + 1], vertices[4 * i + 2], vertices[4 * i + 3]])
            ties.extend([vertices2[4 * i], vertices2[4 * i + 1], vertices2[4 * i + 2], vertices2[4 * i + 3]])
        print("ties", ties)

        for i in range(1000):
            self.indiciesFill2.extend([i])
            colors2.extend([1, 1, 1])

        # Color data for the cube.


        # Convert data to GLSL form and get machine sizes of data types.
        indexdata = np.array(self.indiciesFill).astype(ctypes.c_uint)
        indexdata2 = np.array(self.indiciesFill2).astype(ctypes.c_uint)
        vertexdata = np.array(vertices).astype(ctypes.c_float)
        vertexdata2 = np.array(vertices2).astype(ctypes.c_float)
        tiesdata = np.array(ties).astype(ctypes.c_float)
        colordata = np.array(colors).astype(ctypes.c_float)
        colordata2 = np.array(colors2).astype(ctypes.c_float)
        floatsz = ctypes.sizeof(ctypes.c_float)
        uintsz = ctypes.sizeof(ctypes.c_uint)

        self.insideVAO = glGenVertexArrays(1)
        self.outsideVAO = glGenVertexArrays(1)
        self.railVAO = glGenVertexArrays(1)
        self.BoxEBO = glGenBuffers(3)
        self.InsideArrayBuffer = glGenBuffers(1)
        self.OutsideArrayBuffer = glGenBuffers(1)
        self.RailArrayBuffer = glGenBuffers(1)
        #self.BoxEBO = glGenBuffers(1)


        # Bind (turn on) a vertex array.
        glBindVertexArray(self.outsideVAO)
        # Bind (turn on) a vertex array.
        #glBindVertexArray(self.railVAO)

        # Load the indexing arrays on the graphics card. Load the fill index array.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[0])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(self.indiciesFill), indexdata, GL_STATIC_DRAW)

        # Load the outline index array.
        #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[1])
        #glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(indicesOutline), indexoutlinedata, GL_STATIC_DRAW)

        # Bind (turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.OutsideArrayBuffer)

        # Allocate space for the vertex and color data.Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(vertices) + len(colors)), None, GL_DYNAMIC_DRAW)

        # Load the data vertex at the beginning and then color at the end.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(vertices), vertexdata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(vertices), floatsz * len(colors), colordata)

        # Setup attribute information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vPosition, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribPointer(vColor, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(vertices)))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vColor)

        # Bind (turn on) a vertex array.
        glBindVertexArray(self.insideVAO)

        # Load the indexing arrays on the graphics card. Load the fill index array.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(self.indiciesFill), indexdata, GL_STATIC_DRAW)

        # Bind (turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.InsideArrayBuffer)

        # Allocate space for the vertex and color data.Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(vertices2) + len(colors)), None, GL_DYNAMIC_DRAW)

        # Load the data vertex at the beginning and then color at the end.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(vertices2), vertexdata2)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(vertices2), floatsz * len(colors), colordata)

        # Setup attribute information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vPosition, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribPointer(vColor, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(vertices2)))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vColor)
        # Bind (turn on) a vertex array.

        glBindVertexArray(self.railVAO)

        # Load the indexing arrays on the graphics card. Load the fill index array.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[2])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(self.indiciesFill2), indexdata2, GL_STATIC_DRAW)

        # Bind (turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.RailArrayBuffer)

        # Allocate space for the vertex and color data.Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(ties) + len(colors2)), None, GL_DYNAMIC_DRAW)

        # Load the data vertex at the beginning and then color at the end.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(ties), tiesdata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(ties), floatsz * len(colors2), colordata2)

        # Setup attribute information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vPosition, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribPointer(vColor, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(ties)))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vColor)

    # Draw the Cube.
    def draw(self):
        glBindVertexArray(self.outsideVAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[0])
        glDrawElements(GL_LINE_LOOP, len(self.indiciesFill), GL_UNSIGNED_INT, None)

        glBindVertexArray(self.insideVAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[1])
        glDrawElements(GL_LINE_LOOP, len(self.indiciesFill), GL_UNSIGNED_INT, None)

        glBindVertexArray(self.railVAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[2])
        glDrawElements(GL_LINES, len(self.indiciesFill) * 2, GL_UNSIGNED_INT, None)



