"""
    Author: Anthony Melin
    Date: 2019 August 14
"""

# -*- coding: utf-8 -*-


try:
    from Base import *
except:
    from Scenario.Base import *


import numpy as np
import glm
import time
from Utils import length2D


####################################################################
####################################################################
####################################################################
class SimpleNATDebug(BaseScenario):

    left_area_set = False
    right_area_set = False
    area_range = 0.2

    distractors = ("Fork")
    left_objects = ("Lunchbox", "Bottle")
    right_objects = ("Notebook", "Pen")


    ################################################################
    def Action(self):

        self.NewDetections()

        if not self.left_area_set or not self.right_area_set:
            self.SetAreas()
        else:
            self.SortObjects()


    ################################################################
    def NewDetections(self):

        for obj in self.first_detection:
            pos = self.obj[obj]
            self.socket.Draw("new_text", pos.x, pos.y, pos.z, obj)


    ################################################################
    def SetAreas(self):

        for obj, pos in self.obj.items():

            if obj == "Left" and not self.left_area_set:
                self.left_area_set = True
                self.excluded_detection.append("Left")
                self.socket.Draw("new_area", pos[0], pos[1], pos[2], "left", self.area_range, "gray")

            elif obj == "Right" and not self.right_area_set:
                self.right_area_set = True
                self.excluded_detection.append("Right")
                self.socket.Draw("new_area", pos[0], pos[1], pos[2], "right", self.area_range, "gray")


    ################################################################
    def SortObjects(self):

        # update texts color
        for obj, pos in self.obj.items():

            # object to put in left area
            if obj in self.left_objects:
                self.LeftAreaObject(obj, pos)

            # object to put in right area
            elif obj in self.right_objects:
                self.RightAreaObject(obj, pos)

            # distractor
            elif obj in self.distractors:
                self.DistractorObject(obj, pos)

            # for other objects not in lists, use transparent color
            else:
                self.OtherObjects(obj, pos)


    ################################################################
    def LeftAreaObject(self, obj, pos):

        if length2D(self.obj[obj], self.obj["Left"]) < self.area_range:
            self.socket.Draw("update_text", pos.x, pos.y, pos.z, obj, "green")

        elif length2D(self.obj[obj], self.obj["Right"]) < self.area_range:
            self.socket.Draw("update_text", pos.x, pos.y, pos.z, obj, "red")

        else:
            self.socket.Draw("update_text", pos.x, pos.y, pos.z, obj, "white")


    ################################################################
    def RightAreaObject(self, obj, pos):

        if length2D(self.obj[obj], self.obj["Right"]) < self.area_range:
            self.socket.Draw("update_text", pos.x, pos.y, pos.z, obj, "green")

        elif length2D(self.obj[obj], self.obj["Left"]) < self.area_range:
            self.socket.Draw("update_text", pos.x, pos.y, pos.z, obj, "red")

        else:
            self.socket.Draw("update_text", pos.x, pos.y, pos.z, obj, "white")


    ################################################################
    def DistractorObject(self, obj, pos):

        if length2D(self.obj[obj], self.obj["Right"]) < self.area_range:
            self.socket.Draw("update_text", pos.x, pos.y, pos.z, obj, "red")

        elif length2D(self.obj[obj], self.obj["Left"]) < self.area_range:
            self.socket.Draw("update_text", pos.x, pos.y, pos.z, obj, "red")

        else:
            self.socket.Draw("update_text", pos.x, pos.y, pos.z, obj, "white")


    ################################################################
    def OtherObjects(self, obj, pos):

        self.socket.Draw("update_text", pos.x, pos.y, pos.z, obj, "alpha")
