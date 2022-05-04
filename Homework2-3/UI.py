#! /usr/bin/env python3
#
# User interface event processing.
#
# Don Spickler
# 11/25/2021

import pygame
from pygame.locals import *
import datetime
from GraphicsEngine import *
import random


class UI():
    # Constructor, links the graphics engine to the user interface for easy
    # one-way communication from the UI to the GE.
    def __init__(self, GE):
        self.ge = GE
        # Set the initial repeat rate time and repeat speed.
        pygame.key.set_repeat(500, 25)

    def processEvents(self, event):
        if event.type == KEYDOWN:
            self.processKeydown(event)

        if event.type == MOUSEBUTTONDOWN:
            key = pygame.key.get_pressed()
            btnDown = self.processMouseButtonDown(event)
            rbtn = self.processRightMouseButtonDown(event)
            leftBtn = self.processMouseButtonDown(event)

            if btnDown and not (key[K_LSHIFT] or key[K_RSHIFT]):
                for i in range(len(self.ge.boxes)):
                    self.ge.boxes[self.ge.boxNum].oldMousePosition = self.MouseToScreenConversion(pygame.mouse.get_pos())
                    print("clicked here", self.ge.box.oldMousePosition)

            if btnDown and (key[K_LSHIFT] or key[K_RSHIFT]):
                for i in range(len(self.ge.selected)):
                    self.ge.selected[i].oldMousePosition = self.MouseToScreenConversion(pygame.mouse.get_pos())
                    print("clicked here", self.ge.box.oldMousePosition)

            if self.ge.notInBox and rbtn and (key[K_LCTRL] or key[K_RCTRL]):
                self.ge.box.mousePosition = self.MouseToScreenConversion(pygame.mouse.get_pos())
                newWidth = random.uniform(0.1, 0.3)
                newHeight = random.uniform(0.1, 0.3)
                print("got here")
                self.ge.createBox(self.ge.box.mousePosition[0], self.ge.box.mousePosition[1], newWidth, newHeight)
                #self.ge.box.mousePosition.clear()

            elif not self.ge.notInBox and rbtn and (key[K_LCTRL] or key[K_RCTRL]):
                self.ge.deleteBox()

            elif not self.ge.notInBox and leftBtn and (key[K_LCTRL] or key[K_RCTRL]):
                self.ge.toggleBox()
                print("select box")

            elif self.ge.notInBox and leftBtn and (key[K_LCTRL] or key[K_RCTRL]):
                self.ge.selected.clear()

        if event.type == MOUSEMOTION:
            key = pygame.key.get_pressed()
            self.processMouseMotion(event)
            leftBtn = self.processMouseButtonDown(event)
            # print(self.ge.box.mousePosition)

            if leftBtn and not (key[K_LSHIFT] or key[K_RSHIFT]) and not self.ge.notInBox:
                newMousePosition = self.MouseToScreenConversion(pygame.mouse.get_pos())
                #print("new mouse", self.ge.box.mousePosition)
                print("new mouse", newMousePosition)
                self.ge.move(newMousePosition)
                # clear/reset difference
                # move the box
            elif leftBtn and (key[K_LSHIFT] or key[K_RSHIFT]) and not self.ge.notInBox:
                newMousePosition = self.MouseToScreenConversion(pygame.mouse.get_pos())
                for i in range(len(self.ge.selected)):
                    self.ge.selected[i].drag(newMousePosition)

        if event.type == MOUSEBUTTONUP:
            self.processMouseButtonUp(event)

    def processKeydown(self, event):
        if (event.mod & KMOD_CTRL) and (event.mod & KMOD_SHIFT):  # Control and shift down
            # Reset the box center.
            if event.key == K_f:
                self.ge.box.setCenter(0, 0)

        else:  # No modifiers
            # Set the rendering mode to fill.
            if event.key == K_F1:
                self.ge.setFill()

            # Set the rendering mode to line.
            if event.key == K_F2:
                self.ge.setLine()

            # Set the rendering mode to point.
            if event.key == K_F3:
                self.ge.setPoint()

            if event.key == K_F8:
                self.ge.boxes.clear()

            # Get a screen shot and save to png file.
            if event.key == K_F12:
                path = datetime.datetime.now().strftime('ScreenShot_%Y-%m-%d_%H:%M:%S.%f.png')
                image = self.ge.getScreenImage()
                image.save(path)
        """
        elif event.mod & KMOD_SHIFT:  # Shift down
            # Reset the box to original position and size.
            if event.key == K_r:
                self.ge.box.setCenter(0, 0)
                self.ge.box.setSize(1, 1)

        elif event.mod & KMOD_ALT:  # Alt down
            # Reset the box to original position and size.
            if event.key == K_r:
                self.ge.box.setCenter(0, 0)
                self.ge.box.setSize(1, 1)
        """

    def processKeyStates(self):
        key = pygame.key.get_pressed()
        if key[K_LCTRL] or key[K_RCTRL]:  # Either control key down.

            if key[K_a]:
                for i in range(len(self.ge.boxes)):
                    self.ge.selected.append(self.ge.boxes[i])

            if key[K_q]:
                self.ge.selected.clear()

            # Decrease the box width.
            if key[K_LEFT]:
                for i in range(len(self.ge.selected)):
                    w = self.ge.selected[i].getWidth()
                    w = w - 0.01
                    self.ge.selected[i].setWidth(w)

            # Increase the box width.
            if key[K_RIGHT]:
                for i in range(len(self.ge.selected)):
                    w = self.ge.selected[i].getWidth()
                    w = w + 0.01
                    self.ge.selected[i].setWidth(w)

            # Increase the box height.
            if key[K_UP]:
                for i in range(len(self.ge.selected)):
                    h = self.ge.selected[i].getHeight()
                    h = h + 0.01
                    self.ge.selected[i].setHeight(h)

            # Decrease the box height.
            if key[K_DOWN]:
                for i in range(len(self.ge.selected)):
                    h = self.ge.selected[i].getHeight()
                    h = h - 0.01
                    self.ge.selected[i].setHeight(h)

        elif key[K_LALT] or key[K_RALT]:
            if key[K_b]:
                self.ge.box.colors = [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
                self.ge.box.LoadDataToGraphicsCard()
            elif key[K_g]:
                self.ge.box.colors = [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
                self.ge.box.LoadDataToGraphicsCard()
            elif key[K_w]:
                self.ge.box.colors = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                self.ge.box.LoadDataToGraphicsCard()
            elif key[K_m]:
                self.ge.box.colors = [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1]
                self.ge.box.LoadDataToGraphicsCard()
            # Increase the box height.
            elif key[K_UP]:
                for i in range(len(self.ge.selected)):
                    h = self.ge.selected[i].getHeight()
                    w = self.ge.selected[i].getWidth()
                    w = w + 0.01
                    h = h + 0.01
                    self.ge.selected[i].setHeight(h)
                    self.ge.selected[i].setWidth(w)
            # Decrease the box height.
            elif key[K_DOWN]:
                for i in range(len(self.ge.selected)):
                    h = self.ge.selected[i].getHeight()
                    w = self.ge.selected[i].getWidth()
                    w = w - 0.01
                    h = h - 0.01
                    self.ge.selected[i].setHeight(h)
                    self.ge.selected[i].setWidth(w)


        else:  # No modifiers
            # Move box up.
            if key[K_UP]:
                for i in range(len(self.ge.selected)):
                    cx, cy = self.ge.selected[i].getCenter()
                    cy = cy + 0.01
                    self.ge.selected[i].setCenter(cx, cy)

            # Move box down.
            if key[K_DOWN]:
                for i in range(len(self.ge.selected)):
                    cx, cy = self.ge.selected[i].getCenter()
                    cy = cy - 0.01
                    self.ge.selected[i].setCenter(cx, cy)

            # Move box left.
            if key[K_LEFT]:
                for i in range(len(self.ge.selected)):
                    cx, cy = self.ge.selected[i].getCenter()
                    cx = cx - 0.01
                    self.ge.selected[i].setCenter(cx, cy)

            # Move box right.
            if key[K_RIGHT]:
                for i in range(len(self.ge.selected)):
                    cx, cy = self.ge.selected[i].getCenter()
                    cx = cx + 0.01
                    self.ge.selected[i].setCenter(cx, cy)

    def processMouseMotion(self, event):
        screenPos = self.MouseToScreenConversion(pygame.mouse.get_pos())
        self.ge.coordinates = [screenPos[0], screenPos[1]]
        # print(event, end=' -- ')
        #print("coordinates", self.ge.coordinates)

    def processMouseButtonDown(self, event):
        mouseButn = pygame.mouse.get_pressed()
        #print(event)
        # print(mouseButn[0])
        return mouseButn[0]

    def processRightMouseButtonDown(self, event):
        mouseButn = pygame.mouse.get_pressed()
        # print(event, end=' -- ')
        # print(mouseButn[0])
        return mouseButn[2]

    def processMouseButtonUp(self, event):
        print(event)

    def processMouseWheel(self, event):
        print(event)

    # Gets the viewport dimensions and input mouse position to convert the mouse location
    # from pixel positions to world positions.
    def MouseToScreenConversion(self, mousePosition):
        x, y = mousePosition
        lx, ux, ly, uy = self.ge.box.getScreenBounds()
        ulx, ulr, w, h = self.ge.box.getViewport()
        screenPos = [x / w * (ux - lx) + lx, uy - y / h * (uy - ly)]
        return screenPos
