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
class SimpleNATRelease(SimpleNATDebug):

    left_color = "gray"
    right_color = "gray"


    ################################################################
    def NewDetections(self):

        pass


    ################################################################
    def SortObjects(self):

        self.left_error = False
        self.right_error = False

        SimpleNATDebug.SortObjects(self)

        self.AreaUpdate()


    ################################################################
    def AreaUpdate(self):

        # left area
        if self.left_error and self.left_color == "gray":
            self.left_color = "red"
            self.socket.Draw("update_area", "left", "red")
        elif not self.left_error and self.left_color == "red":
            self.left_color = "gray"
            self.socket.Draw("update_area", "left", "gray")

        # right area
        if self.right_error and self.right_color == "gray":
            self.right_color = "red"
            self.socket.Draw("update_area", "right", "red")
        elif not self.right_error and self.right_color == "red":
            self.right_color = "gray"
            self.socket.Draw("update_area", "right", "gray")


    ################################################################
    def LeftAreaObject(self, obj, pos):

        if length2D(self.obj[obj], self.obj["Right"]) < self.area_range:
            self.right_error = True


    ################################################################
    def RightAreaObject(self, obj, pos):

        if length2D(self.obj[obj], self.obj["Left"]) < self.area_range:
            self.left_error = True


    ################################################################
    def DistractorObject(self, obj, pos):

        self.LeftAreaObject(obj, pos)
        self.RightAreaObject(obj, pos)


    ################################################################
    def OtherObjects(self, obj, pos):

        pass
