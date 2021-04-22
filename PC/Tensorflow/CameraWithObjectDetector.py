#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2019 August 14
# -------------------------

# # Global variables

# In[ ]:



# # Import module

# In[ ]:


from ObjectDetection import *
from ObjectDetector import ObjectDetector


# # Global variables
import sys
import os
filedir = os.path.dirname(__file__) #path to this file
pcdir = os.path.join(filedir, os.pardir) #path to NATAssistanceAR/PC
sys.path.insert(1, pcdir)
import GlobalVariables.Settings as settings

# # Load model

# In[ ]:


category_index = load_categories(settings.LABELS, settings.NUM_CLASSES)
sess, inputs, outputs = load_model(settings.GRAPH)


# # Set frame detector

# In[ ]:


detector = ObjectDetector(sess, inputs, outputs, category_index)
detector.SetThreshold(settings.DETECTOR_THRESHOLD)
detector.draw = True


# # Loop

# In[ ]:


import cv2
import numpy as np

video = cv2.VideoCapture(0)
if not video.isOpened(): raise BaseException("Camera not found")

while(True):

    ret, frame = video.read()
    
    detected = detector.Detect(frame)

    cv2.imshow('Object detector', frame)
    if cv2.waitKey(1) == ord(settings.EXIT_KEY): break

video.release()
cv2.destroyAllWindows()

