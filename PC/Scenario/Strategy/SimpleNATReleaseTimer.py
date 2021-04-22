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

####################################################################
####################################################################
####################################################################
class SimpleNATReleaseTimer(SimpleNATRelease):

    timer_left = time.time()
    timer_right = time.time()
    delay = 5

    ################################################################
    def SortObjects(self):

        self.left_error = False
        self.right_error = False

        SimpleNATDebug.SortObjects(self)

        self.CheckErrorDelay()

        self.AreaUpdate()


    ################################################################
    def CheckErrorDelay(self):

        # calc delay in second
        left_delay = time.time() - self.timer_left
        right_delay = time.time() - self.timer_right

        # timer is updated if there is not error detected
        if not self.left_error:
            self.timer_left = time.time()
        # cancel the error as it occurs for less than 5 seconds
        elif left_delay < 5:
            self.left_error = False
        # else the the error will still be treated in AreaUpdate()

        # right area
        if not self.right_error:
            self.timer_right = time.time()
        elif self.right_error and right_delay < 5:
            self.right_error = False