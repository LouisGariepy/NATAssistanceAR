#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2020 January 11
# -------------------------

# # Import

# In[1]:


from RemoteCam.RemoteCam import RemoteCam
from Tensorflow.ObjectDetection import *
from Tensorflow.ObjectDetector import ObjectDetector

from Scenario.Base2D import BaseScenario2D

import cv2
import sys
import numpy as np
import os


# # Global variables
import GlobalVariables.Settings as settings


# ## Scenario
scenario = BaseScenario2D()

# # Object detection configuration

# ### Load model
category_index = load_categories(settings.LABELS, settings.NUM_CLASSES)
sess, inputs, outputs = load_model(settings.GRAPH)


# ### Set frame detector
detector = ObjectDetector(sess, inputs, outputs, category_index)
detector.SetThreshold(settings.DETECTOR_THRESHOLD)
detector.draw = True


# # Loop
camera = RemoteCam(settings.REMOTECAM_PORT, settings.REMOTECAM_NBSOCKETS)

while True:

    # frame
    frame = camera.getFrame()
    
    if frame.shape == (settings.REMOTECAM_WIDTH, settings.REMOTECAM_LENGTH, settings.REMOTECAM_NBSOCKETS):
        
        # detection
        detected = detector.Detect(frame)
        scenario.Update(detected, frame)
    
    # display
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord(settings.EXIT_KEY): break

cv2.destroyAllWindows()
camera.close()


