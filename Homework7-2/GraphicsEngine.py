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

from Cube import *
from Sphere import *
from Torus import *
from Trefoil import *
from Plane import *
from SimplePlane import *
from HeightMap import *
from ModelData import *
from Axes3D import *
from SphericalCamera import *
from YPRCamera import *
from Light import *
from Material import *


class GraphicsEngine():
    mode = GL_FILL
    shaderProgram = -1
    cameranum = 1
    displayobjmode = 1
    showaxes = False
    showlight = False
    textures = True
    turnOnLights = True
    projectionMatrix = glm.mat4(1)
    viewMatrix = glm.mat4(1)

    # Constructor
    def __init__(self):
        # Load shaders and compile shader programs.
        try:
            shader = Shader()
            self.AxesShader = shader.loadShadersFromFile("Shaders/VertexShaderBasic3D.glsl",
                                                         "Shaders/PassThroughFrag.glsl")
            self.TextureShader = shader.loadShadersFromFile("Shaders/VertexShaderLightingTexture.glsl",
                                                            "Shaders/PhongMultipleLightsAndTexture.glsl")
            self.ConstColorShader = shader.loadShadersFromFile("Shaders/VertexShaderBasic3D.glsl",
                                                               "Shaders/ConstantColorFrag.glsl")

        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        # Turn on program, get the locations of some of the uniform variables.
        glUseProgram(self.AxesShader)
        self.projviewLocAxes = glGetUniformLocation(self.AxesShader, "ProjView")
        self.modelLocAxes = glGetUniformLocation(self.AxesShader, "Model")

        glUseProgram(self.TextureShader)
        self.projviewLocPhong = glGetUniformLocation(self.TextureShader, "PV")
        self.modelLocPhong = glGetUniformLocation(self.TextureShader, "Model")
        self.normalMatrixLocPhong = glGetUniformLocation(self.TextureShader, "NormalMatrix")
        GlobalAmbient = glm.vec4(0.2, 0.2, 0.2, 1)
        glUniform4fv(glGetUniformLocation(self.TextureShader, "GlobalAmbient"),
                     1, glm.value_ptr(GlobalAmbient))
        glUniform1i(glGetUniformLocation(self.TextureShader, "numLights"), 3)
        self.texLocRender = glGetUniformLocation(self.TextureShader, "tex1")
        self.texYNLocRender = glGetUniformLocation(self.TextureShader, "useTexture")

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

        # Create the cameras.
        self.sphericalcamera = SphericalCamera(30, 60, 45)
        self.yprcamera = YPRCamera()
        self.setViewMatrix()

        # Create and load the objects.
        self.axes = Axes3D()


        self.sphere = Sphere()
        # self.sphere = Sphere(1, 20, 20, glm.radians(45), glm.radians(200), glm.radians(-45), glm.radians(45))

        self.lightsphere = Sphere(0.25, 10, 10)

        self.torus = Torus()
        # self.torus.set(1.5, 2, 50, 20)

        self.trefiol = Trefoil()

        self.plane = Plane()
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

        self.simpleplane = SimplePlane()

        # Load Lights and Materials

        self.mat = Material()
        #self.mat.Copper()

        self.lights = []
        self.lights.append(Light())
        self.lightcamera = YPRCamera(glm.vec3(0, 0, -1))

        # Set light positions.  Light 0 will ne locked to the lightcamera object.
        self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)

        # Tone down the intensity of the lights.
        # lightFactor = 1
        lightFactor = 0.75

        self.lights[0].diffuse = lightFactor * self.lights[0].diffuse
        self.lights[0].specular = lightFactor * self.lights[0].specular

        self.mat.LoadMaterial(self.TextureShader, "Mat")


        # Load in texture.

        # teximg = Image.open("Images/cat001.png")
        # teximg = Image.open("Images/cat002.png")
        # teximg = Image.open("Images/cat003.png")
        # teximg = Image.open("Images/cat004.png")
        # teximg = Image.open("Images/amazaque.bmp")
        # teximg = Image.open("Images/lrock023.bmp")
        # teximg = Image.open("Images/misc026.bmp")
        # teximg = Image.open("Images/misc107.bmp")
        # teximg = Image.open("Images/misc151.bmp")
        # teximg = Image.open("Images/misc152.bmp")
        teximg = Image.open("Images/metal024.bmp")
        # teximg = Image.open("Images/Repeat-brick.jpg")

        teximg = teximg.convert('RGBA')
        teximg = teximg.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(teximg.getdata()), np.int8)

        self.texID = glGenTextures(6)
        self.texID[0] = self.loadTexture("Images/HW007_Textures/Prob2_Textures/metal024.bmp")
        self.texID[1] = self.loadTexture("Images/HW007_Textures/Prob2_Textures/metal024.bmp")

        """
        # Link the texture ID to different texture units.
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texID[:2])
        """



        self.texID[2] = self.loadTexture("Images/HW007_Textures/Prob2_Textures/misc152.bmp")
        self.texID[3] = self.loadTexture("Images/HW007_Textures/Prob2_Textures/misc026.bmp")
        self.texID[4] = self.loadTexture("Images/HW007_Textures/Prob2_Textures/Repeat-brick.jpg")
        self.texID[5] = self.loadTexture("Images/HW007_Textures/Prob2_Textures/Repeat-brick.jpg")

        """
        # Link the texture ID to different texture units.
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texID[2:])
        """


        glActiveTexture(GL_TEXTURE0)
        self.PictureCube = PictureCube(self.texID)
        #glBindTexture(GL_TEXTURE_2D, self.texID[1])
        """
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, teximg.width, teximg.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        """

        glUniform1i(self.texLocRender, 0)
        glUniform1i(self.texYNLocRender, True)

        """
        # Set the texture transformation.
        textureMat = glm.mat4(1)

        textureMat = glm.scale(glm.vec3(300, 10, 10))
        # textureMat = glm.scale(glm.vec3(20, 1, 0))
        # textureMat = glm.rotate(glm.radians(30), glm.vec3(0, 0, 1))
        # textureMat = glm.translate(glm.vec3(0.5, 0.2, 0))

        # Load Texture matrix.  Note that if this is not dynamic it can be loaded outside the update.
        glUniformMatrix4fv(glGetUniformLocation(self.TextureShader, "textrans"), 1, GL_FALSE, glm.value_ptr(textureMat))
        """

    def loadTexture(self, filename):
        teximg = Image.open(filename)
        teximg = teximg.convert('RGBA')
        teximg = teximg.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.asarray(teximg)

        texID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, teximg.width, teximg.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

        return texID
    # Turn on shader, clear screen, draw axes, cubes, or box.
    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)

        # Draw axes if selected.
        if self.showaxes:
            glUseProgram(self.AxesShader)
            axestrans = glm.scale(glm.vec3(10))
            glUniformMatrix4fv(self.modelLocAxes, 1, GL_FALSE, glm.value_ptr(axestrans))
            self.axes.draw()

        # Draw position of the light if selected.

        if self.showlight:
            vector = self.lightcamera.getPosition()
            glUseProgram(self.ConstColorShader)
            self.lights[0].position = glm.vec4(vector[0], vector[1], vector[2] + -5.0, 1)

            lightobjmodel = glm.translate(glm.vec3(self.lights[0].position))
            glUniformMatrix4fv(self.modelLocConst, 1, GL_FALSE, glm.value_ptr(lightobjmodel))
            self.lightsphere.draw()




        # Draw remainder of scene.
        glUseProgram(self.TextureShader)

        # Set the light position from the light "camera". Load to shader.
        self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)
        self.lights[0].LoadLight(self.TextureShader, "Lt[0]")

        # Get the position of the camera and load to the shader.
        eye = glm.vec3(0, 0, 0)

        if self.cameranum == 0:
            eye = self.sphericalcamera.getPosition()
        elif self.cameranum == 1:
            eye = self.yprcamera.getPosition()


        glUniform3fv(glGetUniformLocation(self.TextureShader, "eye"), 1, glm.value_ptr(eye))

        # glUseProgram(self.LightingShader3)
        model = glm.mat4(1.0)
        model = glm.scale(model, glm.vec3(10, 10, 990))
        #model = glm.scale(model, glm.vec3(10, 1, 10))

        self.LoadMatrices(model)
        self.PictureCube.draw(self.textures, self.TextureShader)

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

    # Loads the model matrix, calculates the normal matrix, (M^(-1))^T, and loads
    # it to the shader.  Function assumes that the lighting shader program is active.
    def LoadMatrices(self, model):
        glUniformMatrix4fv(self.modelLocPhong, 1, GL_FALSE, glm.value_ptr(model))
        NM = glm.inverse(glm.transpose(glm.mat3(model)))
        glUniformMatrix3fv(self.normalMatrixLocPhong, 1, GL_FALSE, glm.value_ptr(NM))

    # Set and load the projection matrix to the graphics card.
    def setProjectionMatrix(self, size):
        w, h = size
        self.projectionMatrix = glm.perspective(glm.radians(50.0), w / h, 0.01, 500.0)
        PV = self.projectionMatrix * self.viewMatrix
        glUseProgram(self.AxesShader)
        glUniformMatrix4fv(self.projviewLocAxes, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.TextureShader)
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
        glUniformMatrix4fv(self.projviewLocAxes, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.TextureShader)
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

    # Toggle the drawing of the textures.
    def toggleTextures(self):
        self.textures = not self.textures
        glUniform1i(glGetUniformLocation(self.TextureShader, "useTexture"), self.textures)

    # Toggle the drawing of the axes.
    def toggleLight(self):
        self.showlight = not self.showlight

    def toggleLightUse(self):
        self.turnOnLights = not self.turnOnLights
        for i in range(3):
            self.lights[i].on = self.turnOnLights
            self.lights[i].LoadLight(self.TextureShader, "Lt[" + str(i) + "]")

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
