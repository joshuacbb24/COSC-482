#! /usr/bin/env python3
#
# User interface event processing.
#
# Don Spickler
# 12/30/2021

import pygame
from pygame.locals import *
import datetime
from GraphicsEngine import *


class UI():
    # Constructor, links the graphics engine to the user interface for easy
    # one-way communication from the UI to the GE.
    def __init__(self, GE):
        self.ge = GE
        # Set the initial repeat rate time and repeat speed.
        pygame.key.set_repeat(500, 25)
        self.outline = False
        self.lastMousePosition = (0, 0)

    def processEvents(self, event):
        if event.type == KEYDOWN:
            self.processKeydown(event)

        if event.type == pygame.VIDEORESIZE:
            self.ge.setProjectionMatrix(event.size)

        if event.type == MOUSEMOTION:
            self.processMouseMotion(event)

        if event.type == MOUSEBUTTONDOWN:
            self.processMouseButtonDown(event)

        # if event.type == MOUSEBUTTONUP:
        #     self.processMouseButtonUp(event)

        if event.type == MOUSEWHEEL:
            self.processMouseWheel(event)

    def processKeydown(self, event):
        # Toggle the camera between spherical and YPR.
        if event.key == K_c:
            self.ge.toggleCamera()
            self.ge.setViewMatrix()

        # Toggle the drawing of the objects between fill and outline.
        if event.key == K_o:
            self.outline = not self.outline
            if self.outline:
                self.ge.box.drawStyle = 1
                self.ge.cube.drawStyle = 1
            else:
                self.ge.box.drawStyle = 0
                self.ge.cube.drawStyle = 0

        # Toggle the drawing of the axes.
        if event.key == K_l:
            self.ge.toggleAxes()

        # Draw the grid of cubes.
        if event.key == K_1:
            self.ge.displayobjmode = 1

        # Draw a single cube.
        if event.key == K_2:
            self.ge.displayobjmode = 2

        # Draw a single 2D box.
        if event.key == K_3:
            self.ge.displayobjmode = 3
        # Draw the grid of cubes.
        if event.key == K_4:
            self.ge.displayobjmode = 4

        # Draw a single cube.
        if event.key == K_5:
            self.ge.displayobjmode = 5

        # Draw a single 2D box.
        if event.key == K_6:
            self.ge.displayobjmode = 6
        # Draw the grid of cubes.
        if event.key == K_7:
            self.ge.displayobjmode = 7

        # Draw a single cube.
        if event.key == K_8:
            self.ge.displayobjmode = 8

        # Draw a single 2D box.
        if event.key == K_9:
            self.ge.displayobjmode = 9
        if event.key == K_0:
            self.ge.displayobjmode = 0
        # Set the rendering mode to fill.
        if event.key == K_F1:
            self.ge.setFill()

        # Set the rendering mode to line.
        if event.key == K_F2:
            self.ge.setLine()

        # Set the rendering mode to point.
        if event.key == K_F3:
            self.ge.setPoint()

        # Get a screen shot and save to png file.
        if event.key == K_F12:
            path = datetime.datetime.now().strftime('ScreenShot_%Y-%m-%d_%H-%M-%S.%f.png')
            image = self.ge.getScreenImage()
            image.save(path)

    # Process key states by the currently selected camera.
    def processKeyStates(self):
        if self.ge.cameranum == 0:
            self.StateProcessingSphericalCamera()
        else:
            self.StateProcessingYPRCamera()

    # State processing for the spherical camera.
    def StateProcessingSphericalCamera(self):
        key = pygame.key.get_pressed()
        if key[K_LCTRL] or key[K_RCTRL] or key[K_z]:  # Either control key or Z is down.
            # Decrease the camera radius.
            if key[K_UP]:
                self.ge.sphericalcamera.addR(-0.1)
                self.ge.setViewMatrix()

            # Increase the camera radius.
            if key[K_DOWN]:
                self.ge.sphericalcamera.addR(0.1)
                self.ge.setViewMatrix()
        else:
            # Increase the camera psi.
            if key[K_UP]:
                self.ge.sphericalcamera.addPsi(1)
                self.ge.setViewMatrix()

            # Decrease the camera psi.
            if key[K_DOWN]:
                self.ge.sphericalcamera.addPsi(-1)
                self.ge.setViewMatrix()

            # Increase the camera theta.
            if key[K_LEFT]:
                self.ge.sphericalcamera.addTheta(1)
                self.ge.setViewMatrix()

            # Decrease the camera theta.
            if key[K_RIGHT]:
                self.ge.sphericalcamera.addTheta(-1)
                self.ge.setViewMatrix()

    # State processing for the YPR camera.
    def StateProcessingYPRCamera(self):
        key = pygame.key.get_pressed()
        if key[K_LCTRL] or key[K_RCTRL] or key[K_z]:  # Either control key or Z is down.
            # Increase the roll.
            if key[K_LEFT]:
                self.ge.yprcamera.addRoll(1)
                self.ge.setViewMatrix()

            # Decrease the roll.
            if key[K_RIGHT]:
                self.ge.yprcamera.addRoll(-1)
                self.ge.setViewMatrix()

            # Move forward.
            if key[K_UP]:
                self.ge.yprcamera.moveForward(0.1)
                self.ge.setViewMatrix()

            # Move backward.
            if key[K_DOWN]:
                self.ge.yprcamera.moveForward(-0.1)
                self.ge.setViewMatrix()

        elif key[K_LSHIFT] or key[K_RSHIFT] or key[K_s]:  # Either Shift key or S is down.
            # Move left.
            if key[K_LEFT]:
                self.ge.yprcamera.moveRight(-0.1)
                self.ge.setViewMatrix()

            # Move right.
            if key[K_RIGHT]:
                self.ge.yprcamera.moveRight(0.1)
                self.ge.setViewMatrix()

            # Move up.
            if key[K_UP]:
                self.ge.yprcamera.moveUp(0.1)
                self.ge.setViewMatrix()

            # Move down.
            if key[K_DOWN]:
                self.ge.yprcamera.moveUp(-0.1)
                self.ge.setViewMatrix()
        else:
            # Increase the yaw.
            if key[K_LEFT]:
                self.ge.yprcamera.addYaw(1)
                self.ge.setViewMatrix()

            # Decrease the yaw.
            if key[K_RIGHT]:
                self.ge.yprcamera.addYaw(-1)
                self.ge.setViewMatrix()

            # Increase the pitch.
            if key[K_UP]:
                self.ge.yprcamera.addPitch(1)
                self.ge.setViewMatrix()

            # Decrease the pitch.
            if key[K_DOWN]:
                self.ge.yprcamera.addPitch(-1)
                self.ge.setViewMatrix()

    def processMouseMotion(self, event):
        mousescale = 5
        buttons = pygame.mouse.get_pressed()
        key = pygame.key.get_pressed()

        if buttons[0]:
            x, y = pygame.mouse.get_pos()

            x -= self.lastMousePosition[0]
            y -= self.lastMousePosition[1]

            x /= mousescale
            y /= mousescale

            if self.ge.cameranum == 0:
                # Increase or decrease the radius of the camera from the origin.
                if key[K_LCTRL] or key[K_RCTRL]:
                    self.ge.sphericalcamera.addR(-y)
                    self.ge.setViewMatrix()
                else:
                    # Alter the theta and psi values of the camera.
                    self.ge.sphericalcamera.addTheta(x)
                    self.ge.sphericalcamera.addPsi(y)
                    self.ge.setViewMatrix()
            else:
                # Increase or decrease the roll.
                if (key[K_LSHIFT] or key[K_RSHIFT]) and (key[K_LCTRL] or key[K_RCTRL]):
                    self.ge.yprcamera.addRoll(x)
                    self.ge.setViewMatrix()
                elif key[K_LCTRL] or key[K_RCTRL]:
                    # Move forward o backward.
                    self.ge.yprcamera.moveForward(-y)
                    self.ge.setViewMatrix()
                elif key[K_LSHIFT] or key[K_RSHIFT]:
                    # Move left/right and up/down.
                    self.ge.yprcamera.moveRight(-x)
                    self.ge.yprcamera.moveUp(y)
                    self.ge.setViewMatrix()
                else:
                    # Alter the yaw and pitch.
                    self.ge.yprcamera.addYaw(x)
                    self.ge.yprcamera.addPitch(y)
                    self.ge.setViewMatrix()

            self.lastMousePosition = pygame.mouse.get_pos()

    def processMouseButtonDown(self, event):
        self.lastMousePosition = pygame.mouse.get_pos()

    # def processMouseButtonUp(self, event):
    #     print(event)

    def processMouseWheel(self, event):
        mousescale = 1
        y = event.y / mousescale

        # Increase or decrease the radius of the camera from the origin.
        if self.ge.cameranum == 0:
            self.ge.sphericalcamera.addR(-y)
            self.ge.setViewMatrix()
        else:
            # Move forward o backward.
            self.ge.yprcamera.moveForward(-y)
            self.ge.setViewMatrix()
