#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Thomas Leonardon, Pierre-Baptiste Cougnenc, Dylan Mielot, Anthony Melin
# ### Date: 2020 April 5
# -------------------------

# # Import


from RemoteCam.RemoteCam import RemoteCam
from Tensorflow.ObjectDetection import *
from Tensorflow.ObjectDetector import ObjectDetector

from Scenario.PenNearNotebookOnto2D import PenNearNotebookOnto2D

import cv2
import sys
import numpy as np


# # Global variables
import GlobalVariables.Settings as settings


# ## Scenario

scenario = PenNearNotebookOnto2D()
scenario.LoadOnto("Ontology/PenNearNotebook.owl")


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
    
    if frame.shape == (settings.REMOTECAM_WIDTH, settings.REMOTECAM_LENGTH, settings.REMOTECAM_DIM):
        
        # detection
        detected = detector.Detect(frame)
        scenario.Update(detected, frame)
    
    # display
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord(settings.EXIT_KEY): break

cv2.destroyAllWindows()
camera.close()
