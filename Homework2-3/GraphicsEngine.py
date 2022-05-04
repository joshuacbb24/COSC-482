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
from Box import *


class GraphicsEngine():
    # "Addresses" for OpenGL constructs.
    VAO = 0
    Buffer = 0
    vPosition = 0
    vColor = 1
    mode = GL_FILL
    shaderProgram = -1

    # Constructor
    def __init__(self):
        self.boxes = []
        self.coordinates = []
        self.selected = []
        self.InBox = False
        self.notInBox = True
        self.boxNum = None
        self.oldMousePosition = []
        # Load shaders and compile shader programs.
        try:
            shader = Shader()
            self.shaderProgram = shader.loadShadersFromFile("PassThroughVert.glsl", "PassThroughFrag.glsl")
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        # Set clear/background color to black.
        glClearColor(0, 0, 0, 1)

        #self.box = Box()
        #del self.box

        # Create and load the object.
        self.box = Box()

    # Turn on shader, clear screen, draw triangles, swap display buffers.
    def update(self):
        glUseProgram(self.shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)
        self.notInBox = True
        for i in range(len(self.boxes)):
            self.boxes[i].draw()
            if self.coordinates:
                self.InBox = self.boxes[i].inBox(self.coordinates, False)
                if self.InBox:
                    self.notInBox = False
                    self.boxNum = i
        for i in range(len(self.selected)):
            self.selected[i].selectBox()
            self.selBox = self.selected[i].inBox(self.coordinates, True)

        #print("not in box", self.notInBox)
        #print("boxNum", self.boxNum)

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

    def createBox(self, x, y, wd, ht):
        self.box = Box(x, y, wd, ht)
        self.boxes.append(self.box)

    def deleteBox(self):
        del self.boxes[self.boxNum]

    def toggleBox(self):
        found = False
        for i in range(len(self.selected)):
            if self.selected[i] == self.boxes[self.boxNum]:
                found = True
                x = i
        if not found:
            self.selected.append(self.boxes[self.boxNum])
        else:
            del self.selected[x]

        print(self.selected)

    def move(self, newPos):
        #print("in move", self.oldMousePosition)
        self.boxes[self.boxNum].drag(newPos)
        #self.oldMousePosition = [newPos[0], newPos[1]]
        print("after move", self.oldMousePosition)
