#! /usr/bin/env python3
#
# Graphics engine object.
#
# Don Spickler
# 1/8/2022

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from Shader import *
import pygame
import numpy as np
import ctypes
from PIL import Image
import glm
import time
import random
import threading

from Cube import *
from Sphere import *
from Torus import *
from Trefoil import *
from Plane import *
from HeightMap import *
from ModelData import *
from Axes3D import *
from SphericalCamera import *
from YPRCamera import *
from Light import *
from Material import *
from Cylinder import *


class GraphicsEngine():
    mode = GL_FILL
    shaderProgram = -1
    cameranum = 0
    displayobjmode = 1
    showaxes = True
    showlight = True
    projectionMatrix = glm.mat4(1)
    viewMatrix = glm.mat4(1)

    # Constructor
    def __init__(self):
        # Load shaders and compile shader programs.
        try:
            shader = Shader()
            self.AxesShader = shader.loadShadersFromFile("Shaders/VertexShaderBasic3D.glsl",
                                                         "Shaders/PassThroughFrag.glsl")
            self.LightingShader = shader.loadShadersFromFile("Shaders/VertexShaderLighting.glsl",
                                                             "Shaders/PhongMultipleLights.glsl")
            self.LightingShader2 = shader.loadShadersFromFile("Shaders/VertexShaderLighting.glsl",
                                                              "Shaders/PhongMultipleLights.glsl")
            self.LightingShader3 = shader.loadShadersFromFile("Shaders/VertexShaderLighting.glsl",
                                                              "Shaders/PhongMultipleLights.glsl")
            self.ConstColorShader = shader.loadShadersFromFile("Shaders/VertexShaderBasic3D.glsl",
                                                               "Shaders/ConstantColorFrag.glsl")
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        # Turn on program, get the locations of some of the uniform variables.
        self.counter = -1
        glUseProgram(self.AxesShader)
        self.projviewLoc = glGetUniformLocation(self.AxesShader, "ProjView")
        self.modelLoc = glGetUniformLocation(self.AxesShader, "Model")

        glUseProgram(self.LightingShader)
        self.projviewLocPhong = glGetUniformLocation(self.LightingShader, "ProjView")
        self.modelLocPhong = glGetUniformLocation(self.LightingShader, "Model")
        self.normalMatrixLocPhong = glGetUniformLocation(self.LightingShader, "NormalMatrix")
        GlobalAmbient = glm.vec4(0.2, 0.2, 0.2, 1)
        glUniform4fv(glGetUniformLocation(self.LightingShader, "GlobalAmbient"),
                     1, glm.value_ptr(GlobalAmbient))
        glUniform1i(glGetUniformLocation(self.LightingShader, "numLights"), 3)


        glUseProgram(self.ConstColorShader)
        self.projviewLocConst = glGetUniformLocation(self.ConstColorShader, "ProjView")
        self.modelLocConst = glGetUniformLocation(self.ConstColorShader, "Model")
        lightcol = glm.vec4(1, 1, 0, 1)
        glUniform4fv(glGetUniformLocation(self.ConstColorShader, "ConstantColor"),
                     1, glm.value_ptr(lightcol))

        self.setProjectionMatrix(pygame.display.get_surface().get_size())

        # Set clear/background color to black and turn on depth testing.
        glClearColor(0, 0, 0, 1)
        # glClearColor(1, 1, 1, 1)
        glEnable(GL_DEPTH_TEST)
        # glEnable(GL_CULL_FACE)

        # Create the cameras.
        self.sphericalcamera = SphericalCamera(30, 60, 45)
        self.yprcamera = YPRCamera()
        self.setViewMatrix()

        # Create and load the objects.
        self.axes = Axes3D()
        self.cube = Cube()

        self.sphere = Sphere()
        # self.sphere = Sphere(1, 20, 20, glm.radians(45), glm.radians(200), glm.radians(-45), glm.radians(45))

        self.lightsphere = Sphere(0.25, 10, 10)

        self.torus = Torus()
        # self.torus.set(1.5, 2, 50, 20)

        self.trefiol = Trefoil()

        self.plane = Plane()

        self.cylinder = Cylinder()


        # self.plane.set(1, 1, 1, 1)

        # img = Image.open("Images/map001.png")
        # img = Image.open("Images/map002.png")
        # img = Image.open("Images/cat001.png")
        # img = Image.open("Images/cat002.png")
        # img = Image.open("Images/hm001.png")
        img = Image.open("Images/hm002.png")
        # img = Image.open("Images/moon.jpg")
        # img = Image.open("Images/us.jpg")
        # img = Image.open("Images/volcano.png")

        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        self.heightmap = HeightMap(img, 10, 10, 2, 100, 100)

        self.teapot = ModelData("Data/teapotDataTNV.txt", "TNV")

        self.mat = Material()
        self.emit = 0
        self.t = .035

        self.lights = []
        for i in range(3):
            self.lights.append(Light())
        self.lightcamera = SphericalCamera(20, 45, 45)

        # Set light positions.  Light 0 will ne locked to the lightcamera object.
        self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)
        self.lights[1].position = glm.vec4(-10, 20, -10, 1)
        self.lights[2].position = glm.vec4(10, -20, -10, 1)

        # Tone down the intensity of the lights.
        # lightFactor = 1
        lightFactor = 0.75
        for i in range(3):
            self.lights[i].diffuse = lightFactor * self.lights[i].diffuse
            self.lights[i].specular = lightFactor * self.lights[i].specular


        self.mat.BluePlastic()
        #self.mat.LoadMaterial(self.LightingShader2, "Mat")
        self.mat.Silver()
        #self.mat.LoadMaterial(self.LightingShader3, "Mat")
        self.mat.LoadMaterial(self.LightingShader, "Mat")

        self.start_time = time.time()
        self.traverse()

    # Loads the model matrix, calculates the normal matrix, (M^(-1))^T, and loads
    # it to the shader.  Function assumes that the lighting shader program is active.
    def LoadMatrices(self, model):
        glUniformMatrix4fv(self.modelLocPhong, 1, GL_FALSE, glm.value_ptr(model))
        NM = glm.inverse(glm.transpose(glm.mat3(model)))
        glUniformMatrix3fv(self.normalMatrixLocPhong, 1, GL_FALSE, glm.value_ptr(NM))
    def traverse(self):
        t = threading.Timer(1.0, self.traverse)
        t.daemon = True
        t.start()
        self.counter += 1
        if self.counter == 8:
            self.counter = 0
    def drawLaser(self, i, tori):
        if tori:
            if self.counter == 0:
                y = 1.25
            if self.counter == 1:
                y = 2.25
            if self.counter == 2:
                y = 3.25
            if self.counter == 3:
                y = 4.25
            if self.counter == 4:
                y = 5.25
            if self.counter == 5:
                y = 6.25
            if self.counter == 6:
                y = 7.25
        else:
            y = 8.25
        if i == 1:
            model2 = glm.mat4(1.0)
            model2 = glm.rotate(model2, np.pi / 2, glm.vec3(0, 1, 0))
            model2 = glm.translate(model2, glm.vec3(5, y, -5.75))
        if i == 2:
            model2 = glm.mat4(1.0)
            model2 = glm.rotate(model2, np.pi / 2, glm.vec3(0, 1, 0))
            model2 = glm.translate(model2, glm.vec3(-5, y, -5.75))
        if i == 3:
            model2 = glm.mat4(1.0)
            model2 = glm.translate(model2, glm.vec3(5, y, -5.75))
        if i == 4:
            model2 = glm.mat4(1.0)
            model2 = glm.translate(model2, glm.vec3(-5, y, -5.75))
        if i == 5:
            model2 = glm.mat4(1.0)
            model2 = glm.rotate(model2, -45 * np.pi / 180, glm.vec3(0, 1, 0))
            model2 = glm.translate(model2, glm.vec3(0, y, -6.3))
            model2 = glm.scale(model2, glm.vec3(1, 1, 1.25))
        if i == 6:
            model2 = glm.mat4(1.0)
            model2 = glm.rotate(model2, 45 * np.pi / 180, glm.vec3(0, 1, 0))
            model2 = glm.translate(model2, glm.vec3(0, y, -6.3))
            model2 = glm.scale(model2, glm.vec3(1, 1, 1.25))

        self.mat.emission = glm.vec4(0, 1, 1, 1)
        self.mat.LoadMaterial(self.LightingShader, "Mat")
        self.LoadMatrices(model2)
        self.cylinder.draw()
    # Turn on shader, clear screen, draw axes, cubes, or box.
    def update(self):
        timeNow = time.time()
        dt = int(timeNow) - int(self.start_time)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)

        # Draw axes if selected.
        if self.showaxes:
            glUseProgram(self.AxesShader)
            axestrans = glm.scale(glm.vec3(10))
            glUniformMatrix4fv(self.modelLoc, 1, GL_FALSE, glm.value_ptr(axestrans))
            self.axes.draw()

        # Draw position of the light if selected.
        if self.showlight:
            glUseProgram(self.ConstColorShader)
            self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)
            for i in range(3):
                lightobjmodel = glm.translate(glm.vec3(self.lights[i].position))
                glUniformMatrix4fv(self.modelLocConst, 1, GL_FALSE, glm.value_ptr(lightobjmodel))
                self.lightsphere.draw()

        # Draw remainder of scene.
        glUseProgram(self.LightingShader)

        # Set the light position from the light "camera". Load to shader.
        self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)
        for i in range(3):
            self.lights[i].LoadLight(self.LightingShader, "Lt[" + str(i) + "]")

        # Get the position of the camera and load to the shader.
        eye = glm.vec3(0, 0, 0)
        if self.cameranum == 0:
            eye = self.sphericalcamera.getPosition()
        elif self.cameranum == 1:
            eye = self.yprcamera.getPosition()

        glUniform3fv(glGetUniformLocation(self.LightingShader, "eye"), 1, glm.value_ptr(eye))

        # Draw selected objects with appropriate transformations.

        glUseProgram(self.LightingShader)

        if self.displayobjmode == 1:
            """
            for i in range(-10, 11, 4):
                for j in range(-10, 11, 4):
                    for k in range(-10, 11, 4):
                        model = glm.translate(glm.vec3(i, j, k))
                        self.LoadMatrices(model)
                        self.cube.draw()
            
            if dt >= self.storedValue:
                threading.Timer(1.0, printit).start()
                self.counter += 1
                self.storedValue += 1
                if self.counter == 8:
                    self.counter = 0
            """
            #glUseProgram(self.LightingShader)
            model = glm.scale(glm.vec3(10))
            self.LoadMatrices(model)
            self.mat.Emerald()
            self.mat.LoadMaterial(self.LightingShader, "Mat")
            self.plane.draw()

            for j in range(4):
                count = -3
                #glUseProgram(self.LightingShader2)
                model = glm.mat4(1.0)
                self.mat.BluePlastic()
                self.mat.LoadMaterial(self.LightingShader, "Mat")
                if j == 0:
                    a = 1
                    b = 1
                elif j == 1:
                    a = -1
                    b = 1
                elif j == 2:
                    a = 1
                    b = -1
                elif j == 3:
                    a = -1
                    b = -1
                for i in range(7):
                    model = glm.rotate(model, np.pi / 2, glm.vec3(1, 0, 0))
                    model = glm.translate(model, glm.vec3(5 * a, 5 * b, (-1 * i) + -1))
                    model = glm.scale(model, glm.vec3(count))
                    self.LoadMatrices(model)
                    if self.counter == i:
                        self.mat.emission = glm.vec4(self.emit, 0, 0, 1)
                        self.mat.LoadMaterial(self.LightingShader, "Mat")
                        self.torus.draw()
                        self.drawLaser(random.randint(1, 6), True)
                    else:
                        self.mat.emission = glm.vec4(0, 0, 0, 1)
                        self.mat.LoadMaterial(self.LightingShader, "Mat")
                        self.torus.draw()
                    model = glm.mat4(1.0)
                    count += .25
                #glUseProgram(self.LightingShader3)
                model = glm.translate(model, glm.vec3(5 * a, 8.1, 5 * b))
                model = glm.scale(model, glm.vec3(1))
                self.LoadMatrices(model)
                self.mat.Silver()
                self.mat.LoadMaterial(self.LightingShader, "Mat")
                if self.counter == 7:
                    self.mat.emission = glm.vec4(self.emit, 0, 0, 1)
                    self.mat.LoadMaterial(self.LightingShader, "Mat")
                    self.sphere.draw()
                    self.drawLaser(random.randint(1, 6), False)
                    """
                    for i in range(7):
                        self.cylindar.draw()
                    """
                else:
                    self.mat.emission = glm.vec4(0, 0, 0, 1)
                    self.mat.LoadMaterial(self.LightingShader, "Mat")
                    self.sphere.draw()
            self.emit += self.t
            if self.emit >= 1.037:
                self.t = -1*self.t
            if self.emit <= 0:
                self.t = -1*self.t
        elif self.displayobjmode == 2:
            model = glm.scale(glm.vec3(10))
            self.LoadMatrices(model)
            self.cube.draw()
        elif self.displayobjmode == 3:
            model = glm.scale(glm.vec3(5))
            self.LoadMatrices(model)
            self.sphere.draw()
        elif self.displayobjmode == 4:
            model = glm.mat4(1.0)
            for i in range(7):
                model = glm.rotate(model, np.pi / 2, glm.vec3(1, 0, 0))
                model = glm.translate(model, glm.vec3(5, 5, (-1 * i) + -1))
                model = glm.scale(model, glm.vec3(2))
                self.LoadMatrices(model)
                self.torus.draw()
                model = glm.mat4(1.0)
        elif self.displayobjmode == 5:
            model = glm.scale(glm.vec3(3))
            self.LoadMatrices(model)
            self.trefiol.draw()
        elif self.displayobjmode == 6:
            model = glm.scale(glm.vec3(10))
            self.LoadMatrices(model)
            self.plane.draw()
        elif self.displayobjmode == 7:
            model = glm.scale(glm.vec3(3))
            model = glm.rotate(model, -np.pi / 2, glm.vec3(1, 0, 0))
            self.LoadMatrices(model)
            self.heightmap.draw()
        elif self.displayobjmode == 8:
            model = glm.scale(glm.vec3(10))
            self.LoadMatrices(model)
            self.teapot.draw()

        elif self.displayobjmode == 9:
            model = glm.scale(glm.vec3(10))
            self.LoadMatrices(model)
            self.cylinder.draw()


        self.printOpenGLErrors()

    # Set mode to fill.
    def setFill(self):
        self.mode = GL_FILL

    # Set mode to line.
    def setLine(self):
        self.mode = GL_LINE

    # Set mode to point.
    def setPoint(self):
        self.mode = GL_POINT

    # Set and load the projection matrix to the graphics card.
    def setProjectionMatrix(self, size):
        w, h = size
        self.projectionMatrix = glm.perspective(glm.radians(50.0), w / h, 0.01, 500.0)
        PV = self.projectionMatrix * self.viewMatrix
        glUseProgram(self.AxesShader)
        glUniformMatrix4fv(self.projviewLoc, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.LightingShader)
        glUniformMatrix4fv(self.projviewLocPhong, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.ConstColorShader)
        glUniformMatrix4fv(self.projviewLocConst, 1, GL_FALSE, glm.value_ptr(PV))

    # Set and load the view matrix to the graphics card.
    def setViewMatrix(self):
        if self.cameranum == 0:
            self.viewMatrix = self.sphericalcamera.lookAt()
        else:
            self.viewMatrix = self.yprcamera.lookAt()

        PV = self.projectionMatrix * self.viewMatrix
        glUseProgram(self.AxesShader)
        glUniformMatrix4fv(self.projviewLoc, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.LightingShader)
        glUniformMatrix4fv(self.projviewLocPhong, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.ConstColorShader)
        glUniformMatrix4fv(self.projviewLocConst, 1, GL_FALSE, glm.value_ptr(PV))

    # Toggle between the two cameras.
    def toggleCamera(self):
        if self.cameranum == 0:
            self.cameranum = 1
        else:
            self.cameranum = 0

    # Toggle the drawing of the axes.
    def toggleAxes(self):
        self.showaxes = not self.showaxes

    # Toggle the drawing of the axes.
    def toggleLight(self):
        self.showlight = not self.showlight

    # Dump screen buffer data to raw pixels and convert to PIL Image object.
    def getScreenImage(self):
        viewport = glGetIntegerv(GL_VIEWPORT)
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(viewport[0], viewport[1], viewport[2], viewport[3], GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (viewport[2], viewport[3]), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        return image

    # Print out any errors in the OpenGL error queue.
    def printOpenGLErrors(self):
        errCode = glGetError()
        while errCode != GL_NO_ERROR:
            errString = gluErrorString(errCode)
            print("OpenGL Error: ", errString, "\n")
            errCode = glGetError()
