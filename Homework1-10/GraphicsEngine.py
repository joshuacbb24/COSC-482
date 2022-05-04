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

oRadius = .8
outerPoints = []
innerPoints = []


class GraphicsEngine():
    # "Addresses" for OpenGL constructs.

    vPosition = 0
    vColor = 1
    mode = GL_FILL
    shaderProgram = -1
    data = []
    points = 5
    colorR = 1.00
    colorG = 0.00
    colorB = 0.00

    # Constructor
    def __init__(self, count=0):
        # Load shaders and compile shader programs.
        try:
            shader = Shader()
            self.shaderProgram = shader.loadShadersFromFile("PassThroughVert.glsl", "PassThroughFrag.glsl")
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        self.VAO = glGenVertexArrays(1)
        self.Buffer = glGenBuffers(1)
        """
        for point in range(points):
            outerPoints.append([(oRadius * np.cos(((point * 2 * np.pi) / points) + np.pi / 2)),
                                (oRadius * np.sin(((point * 2 * np.pi) / points) + np.pi / 2))])
            innerPoints.append([(oRadius / 3 * np.cos(((point * 2 * np.pi) / points) + (np.pi) / 3.38)),
                                (oRadius / 3 * np.sin(((point * 2 * np.pi) / points) + (np.pi) / 3.38))])

        # Data for the two triangles to be displayed. Format is (r, g, b, x, y)
        # for each vertex.
        print("outerPoints", outerPoints)
        print(innerPoints)
        print(range(points))
        for point in range(points):
            print(count)
            self.data.append([1.00, 0.00, 0.00, outerPoints[count][0], outerPoints[count][1]])
            self.data.append([1.00, 1.00, 1.00, innerPoints[count][0], innerPoints[count][1]])
            self.data.append([1.00, 1.00, 1.00, 0, 0])
            if count < points - 1:
                self.data.append([1.00, 0.00, 0.00, outerPoints[count][0], outerPoints[count][1]])
                self.data.append([1.00, 1.00, 1.00, innerPoints[count + 1][0], innerPoints[count + 1][1]])
                self.data.append([1.00, 1.00, 1.00, 0, 0])
            else:
                self.data.append([1.00, 0.00, 0.00, outerPoints[count][0], outerPoints[count][1]])
                self.data.append([1.00, 1.00, 1.00, innerPoints[0][0], innerPoints[0][1]])
                self.data.append([1.00, 1.00, 1.00, 0, 0])
            count += 1
        """
        # Set clear/background color ro black.
        glClearColor(0, 0, 0, 1)

        self.loadStarData(self.points)

    # Turn on shader, clear screen, draw triangles, swap display buffers.
    def update(self):
        glUseProgram(self.shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)
        glDrawArrays(GL_TRIANGLES, 0, len(self.data))

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

    def loadStarData(self, numpoints):
        self.data = []
        oPoints = []
        iPoints = []
        counter = 0
        self.points = numpoints

        for newpoint in range(numpoints):
            oPoints.append([(oRadius * (np.cos(((newpoint * 2 * np.pi) / numpoints) + np.pi / 2))),
                            (oRadius * (np.sin(((newpoint * 2 * np.pi) / numpoints) + np.pi / 2)))])
            iPoints.append([(oRadius / 3 * np.cos(
                ((newpoint * 2 * np.pi) / numpoints) + ((np.pi / numpoints) + (np.pi / 2)))),
                            (oRadius / 3 * np.sin(
                                ((newpoint * 2 * np.pi) / numpoints) + ((np.pi / numpoints) + (np.pi / 2))))])

        # Data for the two triangles to be displayed. Format is (r, g, b, x, y)
        # for each vertex.
        print("outerPoints", oPoints)
        print(iPoints)
        print(range(numpoints))
        for newpoint in range(numpoints):
            print(counter)
            self.data.append([self.colorR, self.colorG, self.colorB, oPoints[counter][0], oPoints[counter][1]])
            self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
            self.data.append([1.00, 1.00, 1.00, 0, 0])

            if counter < numpoints - 1:
                self.data.append([self.colorR, self.colorG, self.colorB, oPoints[counter + 1][0], oPoints[counter + 1][1]])
                self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                self.data.append([1.00, 1.00, 1.00, 0, 0])

            else:
                self.data.append([self.colorR, self.colorG, self.colorB, oPoints[0][0], oPoints[0][1]])
                self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                self.data.append([1.00, 1.00, 1.00, 0, 0])

            counter += 1

        print("data", self.data)
        """
        if self.VAO or self.Buffer:
            glDeleteBuffers(1, self.Buffer)
            glDeleteVertexArrays(1, self.VAO)
        """
        # Create the Vertex Array Object and bind.
        glBindVertexArray(self.VAO)

        # Create the Array Buffer and bind.
        glBindBuffer(GL_ARRAY_BUFFER, self.Buffer)

        # Load the data to the graphics card using numpy to set the data type.
        gpudata = np.array(self.data).astype(ctypes.c_float)
        glBufferData(GL_ARRAY_BUFFER, gpudata.ravel(), GL_STATIC_DRAW)

        # Set the data attributes so the card knows how to interpret the data.
        floatsize = ctypes.sizeof(ctypes.c_float)
        glVertexAttribPointer(self.vColor, 3, GL_FLOAT, GL_TRUE, 5 * floatsize, ctypes.c_void_p(0))
        glVertexAttribPointer(self.vPosition, 2, GL_FLOAT, GL_FALSE, 5 * floatsize, ctypes.c_void_p(3 * floatsize))

        # Enable the arrays and set the "positions" for the shaders.
        glEnableVertexAttribArray(self.vPosition)
        glEnableVertexAttribArray(self.vColor)

    def incrementPoints(self, inc):

        if (2 < self.points < 100) or (self.points == 2 and inc == 1) or \
                (self.points == 100 and inc == -1):
            self.points = self.points + inc
            print("numpoints", self.points)
            self.data = []
            oPoints = []
            iPoints = []
            counter = 0
            for newpoint in range(self.points):
                oPoints.append([(oRadius * (np.cos(((newpoint * 2 * np.pi) / self.points) + np.pi / 2))),
                                (oRadius * (np.sin(((newpoint * 2 * np.pi) / self.points) + np.pi / 2)))])
                iPoints.append([(oRadius / 3 * np.cos(
                    ((newpoint * 2 * np.pi) / self.points) + (((np.pi) / self.points) + (np.pi / 2)))),
                                (oRadius / 3 * np.sin(
                                    ((newpoint * 2 * np.pi) / self.points) + (((np.pi) / self.points) + (np.pi / 2))))])


            # Data for the two triangles to be displayed. Format is (r, g, b, x, y)
            # for each vertex.
            print("outerPoints", oPoints)
            print(iPoints)
            print(range(self.points))
            for newpoint in range(self.points):
                print(counter)
                self.data.append([self.colorR, self.colorG, self.colorB, oPoints[counter][0], oPoints[counter][1]])
                self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                self.data.append([1.00, 1.00, 1.00, 0, 0])

                if counter < self.points - 1:
                    self.data.append(
                        [self.colorR, self.colorG, self.colorB, oPoints[counter + 1][0], oPoints[counter + 1][1]])
                    self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                    self.data.append([1.00, 1.00, 1.00, 0, 0])

                else:
                    self.data.append([self.colorR, self.colorG, self.colorB, oPoints[0][0], oPoints[0][1]])
                    self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                    self.data.append([1.00, 1.00, 1.00, 0, 0])
                counter += 1
            print("data", self.data)

            # Create the Vertex Array Object and bind.
            glBindVertexArray(self.VAO)

            # Create the Array Buffer and bind.
            glBindBuffer(GL_ARRAY_BUFFER, self.Buffer)

            # Load the data to the graphics card using numpy to set the data type.
            gpudata = np.array(self.data).astype(ctypes.c_float)
            glBufferData(GL_ARRAY_BUFFER, gpudata.ravel(), GL_STATIC_DRAW)

            # Set the data attributes so the card knows how to interpret the data.
            floatsize = ctypes.sizeof(ctypes.c_float)
            glVertexAttribPointer(self.vColor, 3, GL_FLOAT, GL_TRUE, 5 * floatsize, ctypes.c_void_p(0))
            glVertexAttribPointer(self.vPosition, 2, GL_FLOAT, GL_FALSE, 5 * floatsize, ctypes.c_void_p(3 * floatsize))

            # Enable the arrays and set the "positions" for the shaders.
            glEnableVertexAttribArray(self.vPosition)
            glEnableVertexAttribArray(self.vColor)

        else:
            print("out of range")

    def incrementRed(self, inc):

        if (0.00 < self.colorR < 1.00) or (self.colorR == 0.00 and inc == 0.01) or \
                (self.colorR == 1.00 and inc == -0.01):
            self.colorR = self.colorR + inc
            self.data = []
            oPoints = []
            iPoints = []
            counter = 0
            for newpoint in range(self.points):
                oPoints.append([(oRadius * (np.cos(((newpoint * 2 * np.pi) / self.points) + np.pi / 2))),
                                (oRadius * (np.sin(((newpoint * 2 * np.pi) / self.points) + np.pi / 2)))])
                iPoints.append([(oRadius / 3 * np.cos(
                    ((newpoint * 2 * np.pi) / self.points) + (((np.pi) / self.points) + (np.pi / 2)))),
                                (oRadius / 3 * np.sin(
                                    ((newpoint * 2 * np.pi) / self.points) + (((np.pi) / self.points) + (np.pi / 2))))])

            # Data for the two triangles to be displayed. Format is (r, g, b, x, y)
            # for each vertex.
            print("outerPoints", oPoints)
            print(iPoints)
            print(range(self.points))

            for newpoint in range(self.points):
                print(counter)
                self.data.append([self.colorR, self.colorG, self.colorB, oPoints[counter][0], oPoints[counter][1]])
                self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                self.data.append([1.00, 1.00, 1.00, 0, 0])

                if counter < self.points - 1:
                    self.data.append(
                        [self.colorR, self.colorG, self.colorB, oPoints[counter + 1][0], oPoints[counter + 1][1]])
                    self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                    self.data.append([1.00, 1.00, 1.00, 0, 0])

                else:
                    self.data.append([self.colorR, self.colorG, self.colorB, oPoints[0][0], oPoints[0][1]])
                    self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                    self.data.append([1.00, 1.00, 1.00, 0, 0])
                counter += 1
            print("data", self.data)

            # Create the Vertex Array Object and bind.
            glBindVertexArray(self.VAO)

            # Create the Array Buffer and bind.
            glBindBuffer(GL_ARRAY_BUFFER, self.Buffer)

            # Load the data to the graphics card using numpy to set the data type.
            gpudata = np.array(self.data).astype(ctypes.c_float)
            glBufferData(GL_ARRAY_BUFFER, gpudata.ravel(), GL_STATIC_DRAW)

            # Set the data attributes so the card knows how to interpret the data.
            floatsize = ctypes.sizeof(ctypes.c_float)
            glVertexAttribPointer(self.vColor, 3, GL_FLOAT, GL_TRUE, 5 * floatsize, ctypes.c_void_p(0))
            glVertexAttribPointer(self.vPosition, 2, GL_FLOAT, GL_FALSE, 5 * floatsize, ctypes.c_void_p(3 * floatsize))

            # Enable the arrays and set the "positions" for the shaders.
            glEnableVertexAttribArray(self.vPosition)
            glEnableVertexAttribArray(self.vColor)

        else:
            print("out of range")

    def incrementGreen(self, inc):

        if (0.00 < self.colorG < 1.00) or (self.colorG == 0.00 and inc == 0.01) or \
                (self.colorG == 1.00 and inc == -0.01):
            self.colorG = self.colorG + inc
            self.data = []
            oPoints = []
            iPoints = []
            counter = 0
            for newpoint in range(self.points):
                oPoints.append([(oRadius * (np.cos(((newpoint * 2 * np.pi) / self.points) + np.pi / 2))),
                                (oRadius * (np.sin(((newpoint * 2 * np.pi) / self.points) + np.pi / 2)))])
                iPoints.append([(oRadius / 3 * np.cos(
                    ((newpoint * 2 * np.pi) / self.points) + (((np.pi) / self.points) + (np.pi / 2)))),
                                (oRadius / 3 * np.sin(
                                    ((newpoint * 2 * np.pi) / self.points) + (((np.pi) / self.points) + (np.pi / 2))))])

            # Data for the two triangles to be displayed. Format is (r, g, b, x, y)
            # for each vertex.
            print("outerPoints", oPoints)
            print(iPoints)
            print(range(self.points))

            for newpoint in range(self.points):
                print(counter)
                self.data.append([self.colorR, self.colorG, self.colorB, oPoints[counter][0], oPoints[counter][1]])
                self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                self.data.append([1.00, 1.00, 1.00, 0, 0])

                if counter < self.points - 1:
                    self.data.append(
                        [self.colorR, self.colorG, self.colorB, oPoints[counter + 1][0], oPoints[counter + 1][1]])
                    self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                    self.data.append([1.00, 1.00, 1.00, 0, 0])

                else:
                    self.data.append([self.colorR, self.colorG, self.colorB, oPoints[0][0], oPoints[0][1]])
                    self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                    self.data.append([1.00, 1.00, 1.00, 0, 0])
                counter += 1
            print("data", self.data)

            # Create the Vertex Array Object and bind.
            glBindVertexArray(self.VAO)

            # Create the Array Buffer and bind.
            glBindBuffer(GL_ARRAY_BUFFER, self.Buffer)

            # Load the data to the graphics card using numpy to set the data type.
            gpudata = np.array(self.data).astype(ctypes.c_float)
            glBufferData(GL_ARRAY_BUFFER, gpudata.ravel(), GL_STATIC_DRAW)

            # Set the data attributes so the card knows how to interpret the data.
            floatsize = ctypes.sizeof(ctypes.c_float)
            glVertexAttribPointer(self.vColor, 3, GL_FLOAT, GL_TRUE, 5 * floatsize, ctypes.c_void_p(0))
            glVertexAttribPointer(self.vPosition, 2, GL_FLOAT, GL_FALSE, 5 * floatsize, ctypes.c_void_p(3 * floatsize))

            # Enable the arrays and set the "positions" for the shaders.
            glEnableVertexAttribArray(self.vPosition)
            glEnableVertexAttribArray(self.vColor)

        else:
            print("out of range")

    def incrementBlue(self, inc):

        if (0.00 < self.colorB < 1.00) or (self.colorB == 0.00 and inc == 0.01) or \
                (self.colorB == 1.00 and inc == -0.01):
            self.colorB = self.colorB + inc
            self.data = []
            oPoints = []
            iPoints = []
            counter = 0
            for newpoint in range(self.points):
                oPoints.append([(oRadius * (np.cos(((newpoint * 2 * np.pi) / self.points) + np.pi / 2))),
                                (oRadius * (np.sin(((newpoint * 2 * np.pi) / self.points) + np.pi / 2)))])
                iPoints.append([(oRadius / 3 * np.cos(
                    ((newpoint * 2 * np.pi) / self.points) + (((np.pi) / self.points) + (np.pi / 2)))),
                                (oRadius / 3 * np.sin(
                                    ((newpoint * 2 * np.pi) / self.points) + (((np.pi) / self.points) + (np.pi / 2))))])

            # Data for the two triangles to be displayed. Format is (r, g, b, x, y)
            # for each vertex.
            print("outerPoints", oPoints)
            print(iPoints)
            print(range(self.points))

            for newpoint in range(self.points):
                print(counter)
                self.data.append([self.colorR, self.colorG, self.colorB, oPoints[counter][0], oPoints[counter][1]])
                self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                self.data.append([1.00, 1.00, 1.00, 0, 0])

                if counter < self.points - 1:
                    self.data.append(
                        [self.colorR, self.colorG, self.colorB, oPoints[counter + 1][0], oPoints[counter + 1][1]])
                    self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                    self.data.append([1.00, 1.00, 1.00, 0, 0])

                else:
                    self.data.append([self.colorR, self.colorG, self.colorB, oPoints[0][0], oPoints[0][1]])
                    self.data.append([1.00, 1.00, 1.00, iPoints[counter][0], iPoints[counter][1]])
                    self.data.append([1.00, 1.00, 1.00, 0, 0])
                counter += 1
            print("data", self.data)

            # Create the Vertex Array Object and bind.
            glBindVertexArray(self.VAO)

            # Create the Array Buffer and bind.
            glBindBuffer(GL_ARRAY_BUFFER, self.Buffer)

            # Load the data to the graphics card using numpy to set the data type.
            gpudata = np.array(self.data).astype(ctypes.c_float)
            glBufferData(GL_ARRAY_BUFFER, gpudata.ravel(), GL_STATIC_DRAW)

            # Set the data attributes so the card knows how to interpret the data.
            floatsize = ctypes.sizeof(ctypes.c_float)
            glVertexAttribPointer(self.vColor, 3, GL_FLOAT, GL_TRUE, 5 * floatsize, ctypes.c_void_p(0))
            glVertexAttribPointer(self.vPosition, 2, GL_FLOAT, GL_FALSE, 5 * floatsize, ctypes.c_void_p(3 * floatsize))

            # Enable the arrays and set the "positions" for the shaders.
            glEnableVertexAttribArray(self.vPosition)
            glEnableVertexAttribArray(self.vColor)

        else:
            print("out of range")
