"""
    Authors: Thomas Leonardon, Pierre-Baptiste Cougnenc, Dylan Mielot, Anthony Melin
    Date: 2020 May 15
"""

# -*- coding: utf-8 -*-

import cv2

try:
    # when imported from here
    from Base import BaseScenario
except:
    # when imported from outside
    from Scenario.Base import BaseScenario


"""##########################################################################"""
class PenNearNotebook(BaseScenario):


    """######################################################################"""
    def Action(self):

        for obj in self.first_detection:
            pos = self.obj[obj]
            print("                             ", obj, pos)
            self.socket.Draw("new_text", pos.x, pos.y, pos.z, obj)

        for obj in self.obj:
            pos = self.obj[obj] * 0.8
            print(obj, pos)
            self.socket.Draw("update_text", pos.x, pos.y, pos.z, obj, "white")