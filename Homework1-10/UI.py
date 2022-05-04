#! /usr/bin/env python3
#
# User interface event processing.
#
# Don Spickler
# 11/20/2021

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

    def processEvent(self, event):
        # Process key pressed events.
        if event.type == KEYDOWN:
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
                path = datetime.datetime.now().strftime('ScreenShot_%Y-%m-%d_%H:%M:%S.%f.png')
                image = self.ge.getScreenImage()
                image.save(path)

            # Reset the display mode.
            if event.key == K_r:
                pygame.display.set_mode((600, 600), DOUBLEBUF | OPENGL | RESIZABLE | HWSURFACE)


            # Set the number of points
            if event.key == K_2:
                newPoints = 2
                self.ge.loadStarData(newPoints)

            # Set the number of points
            if event.key == K_3:
                newPoints = 3
                self.ge.loadStarData(newPoints)

            # Set the number of points
            if event.key == K_4:
                newPoints = 4
                self.ge.loadStarData(newPoints)

            # Set the number of points
            if event.key == K_5:
                newPoints = 5
                self.ge.loadStarData(newPoints)

            # Set the number of points
            if event.key == K_6:
                newPoints = 6
                self.ge.loadStarData(newPoints)

            # Set the number of points
            if event.key == K_7:
                newPoints = 7
                self.ge.loadStarData(newPoints)

            # Set the number of points
            if event.key == K_8:
                newPoints = 8
                self.ge.loadStarData(newPoints)

            # Set the number of points
            if event.key == K_9:
                newPoints = 9
                self.ge.loadStarData(newPoints)

            # Set the number of points
            if event.key == K_UP:
                newPoints = 1
                self.ge.incrementPoints(newPoints)

            # Set the number of points
            if event.key == K_DOWN:
                newPoints = -1
                self.ge.incrementPoints(newPoints)

            if event.key == K_r:
                newPoints = 0.01
                self.ge.incrementRed(newPoints)

            if event.key == K_t:
                newPoints = -0.01
                self.ge.incrementRed(newPoints)

            if event.key == K_g:
                newPoints = 0.01
                self.ge.incrementGreen(newPoints)

            if event.key == K_h:
                newPoints = -0.01
                self.ge.incrementGreen(newPoints)

            if event.key == K_b:
                newPoints = 0.01
                self.ge.incrementBlue(newPoints)

            if event.key == K_n:
                newPoints = -0.01
                self.ge.incrementBlue(newPoints)