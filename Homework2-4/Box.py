#! /usr/bin/env python3
#
# Box object
#
# Simple rectangle object with OpenGL data loading and drawing interfaces.  The data that
# is being stored is created in two separate arrays, one for vertices and the other for
# color.  These blocks of data are transferred to a single array buffer on the graphics
# card in two separate locations (that is the data is not intermixed) and hence we can
# set up the reading pointers as having tightly packed data. There is also an index array
# of 6 values {0, 3, 2, 0, 2, 1} that represent the vertices that will be drawn in two
# triangles.  So one triangle will use vertices (0, 3, 2) and the other will use vertices
# (0, 2, 1).
#
# Don Spickler
# 11/24/2021

from OpenGL.GL import *
import ctypes
import numpy as np
import random


class Box():
    # Constructor
    def __init__(self, x=0, y=0, wd=0, ht=0):
        self.count = 0
        self.cx = x
        self.cy = y
        self.w = wd
        self.h = ht
        self.screenBounds = [-1, 1, -1, 1]  # Set to the default here but could be a custom setting [lx, ux, ly, uy].
        self.inBound = None  # Whether cursor is in box section. Set to none or false
        self.boxColorR = random.random()
        self.boxColorG = random.random()
        self.boxColorB = random.random()
        self.colors = [self.boxColorR, self.boxColorG, self.boxColorB, self.boxColorR, self.boxColorG, self.boxColorB,
                       self.boxColorR, self.boxColorG, self.boxColorB, self.boxColorR, self.boxColorG, self.boxColorB]
        self.boxColors = []
        # self.vertices = []
        self.indices = []
        self.boxes = []
        self.oldMousePosition = []
        self.vPosition = 0
        self.vColor = 1
        self.BoxVAO = glGenVertexArrays(1)
        self.ArrayBuffer = glGenBuffers(1)
        self.BoxEBO = glGenBuffers(1)

        self.LoadDataToGraphicsCard()
    """
    def __del__(self):
        try:
            glDeleteBuffers(1, self.ArrayBuffer)
            glDeleteBuffers(1, self.BoxEBO)
            glDeleteVertexArrays(1, self.BoxVAO)
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
    """
    # Load vertex, color, and index data to the graphics card.
    def LoadDataToGraphicsCard(self):

        # Vertex and index data for the box, using two triangles.
        self.vertices = [self.cx - self.w / 2, self.cy + self.h / 2,
                         self.cx + self.w / 2, self.cy + self.h / 2,
                         self.cx + self.w / 2, self.cy - self.h / 2,
                         self.cx - self.w / 2, self.cy - self.h / 2
                         ]

        # print(self.boxes)
        # print(len(self.boxes))
        self.indices = [0, 3, 2, 0, 2, 1]

        # Convert data to GLSL form and get machine sizes of data types.
        indexdata = np.array(self.indices).astype(ctypes.c_uint)
        vertexdata = np.array(self.vertices).astype(ctypes.c_float)
        colordata = np.array(self.colors).astype(ctypes.c_float)
        floatsz = ctypes.sizeof(ctypes.c_float)
        uintsz = ctypes.sizeof(ctypes.c_uint)

        # Bind (turn on) a vertex array.
        glBindVertexArray(self.BoxVAO)

        # Load the indexing array on the graphics card.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(self.indices), indexdata, GL_STATIC_DRAW)

        # Bindm(turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)

        # Allocate  space for the vertex and color data.Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(self.vertices) + len(self.colors)), None, GL_DYNAMIC_DRAW)

        # Load the vertex data.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(self.vertices), vertexdata)

        # Load the color data.
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(self.vertices), floatsz * len(self.colors), colordata)

        # Setup vertex data position information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(self.vPosition, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

        # Setup color data position information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(self.vColor, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(self.vertices)))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(self.vPosition)
        glEnableVertexAttribArray(self.vColor)

    def createBox(self, x, y, wd, ht):
        self.cx = x
        self.cy = y
        self.w = wd
        self.h = ht

        self.boxes.append([self.cx - self.w / 2, self.cy + self.h / 2,
                           self.cx + self.w / 2, self.cy + self.h / 2,
                           self.cx + self.w / 2, self.cy - self.h / 2,
                           self.cx - self.w / 2, self.cy - self.h / 2
                           ])
        self.boxColors.append(self.colors)
        self.LoadDataToGraphicsCard()

        # print("new Data", newData)

    # def deleteBox(self):
    # remove box

    # Set the center of the box and reload the data.
    def setCenter(self, x, y):
        self.cx = x
        self.cy = y
        self.LoadDataToGraphicsCard()

    # Return the center of the box.
    def getCenter(self):
        return self.cx, self.cy

    # Set the width of the box and reload the data.
    def setWidth(self, wd):
        self.w = wd
        self.LoadDataToGraphicsCard()

    # Return the width of the box.
    def getWidth(self):
        return self.w

    # Set the height of the box and reload the data.
    def setHeight(self, ht):
        self.h = ht
        self.LoadDataToGraphicsCard()

    # Return the height of the box.
    def getHeight(self):
        return self.h

    # Return the size [width, height] of the box.
    def getSize(self):
        return self.w, self.h

    # Set the size (width x height) of the box and reload the data.
    def setSize(self, wd, ht):
        self.w = wd
        self.h = ht
        self.LoadDataToGraphicsCard()

    # Draw the box.
    def draw(self):
        glBindVertexArray(self.BoxVAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    # Set mode to point.
    def getScreenBounds(self):
        return self.screenBounds

    # Get the current viewport dimensions.
    def getViewport(self):
        return glGetIntegerv(GL_VIEWPORT)

    # Calculate whether cursor is in box.
    def inBox(self, mousePoints, selBox):

        if mousePoints[0] >= self.vertices[0] and mousePoints[1] >= self.vertices[7]:
            if mousePoints[0] <= self.vertices[2] and mousePoints[1] <= self.vertices[3]:
                self.inBound = True
                self.colors = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
                self.LoadDataToGraphicsCard()
                return self.inBound
            else:
                self.inBound = False
                if not selBox:
                    self.colors = [self.boxColorR, self.boxColorG, self.boxColorB, self.boxColorR, self.boxColorG,
                                   self.boxColorB,
                                   self.boxColorR, self.boxColorG, self.boxColorB, self.boxColorR, self.boxColorG,
                                   self.boxColorB]
                else:
                    self.colors = [1, 1, 0, 1, 1, 0,
                                   1, 1, 0, 1, 1, 0]
                self.LoadDataToGraphicsCard()
                return self.inBound
        else:
            self.inBound = False
            if not selBox:
                self.colors = [self.boxColorR, self.boxColorG, self.boxColorB, self.boxColorR, self.boxColorG,
                               self.boxColorB,
                               self.boxColorR, self.boxColorG, self.boxColorB, self.boxColorR, self.boxColorG,
                               self.boxColorB]
            else:
                self.colors = [1, 1, 0, 1, 1, 0,
                               1, 1, 0, 1, 1, 0]
            self.LoadDataToGraphicsCard()
            return self.inBound

    # drag function
    def drag(self, newPos):
        print("in here")
        #print(self.oldMousePosition)
        print("newpos", newPos[0])
        print("oldMousePosition", self.oldMousePosition[0])
        differenceX = newPos[0] - self.oldMousePosition[0]

        differenceY = newPos[1] - self.oldMousePosition[1]

        print("diffx", differenceX)
        print("diffy", differenceY)

        self.cx = (self.cx + differenceX)
        self.cy = (self.cy + differenceY)

        self.LoadDataToGraphicsCard()

        self.oldMousePosition = newPos


    def selectBox(self):

        self.colors = [1, 1, 0, 1, 1, 0,
                       1, 1, 0, 1, 1, 0]
        self.LoadDataToGraphicsCard()
