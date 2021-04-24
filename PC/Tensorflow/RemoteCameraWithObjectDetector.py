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

frame = cv2.resize(cv2.imread("im.jpg"), (settings.DISPLAY_LENGTH, settings.DISPLAY_WIDTH))

detected = detector.Detect(frame)

cv2.imshow('Object detector', frame)
cv2.waitKey(0)

cv2.destroyAllWindows()


# In[ ]:


import cv2
import numpy as np
import time

from RemoteCam import RemoteCam


video = RemoteCam(settings.REMOTECAM_PORT, settings.REMOTECAM_NBSOCKETS)

while(True):

    frame = video.get_frame()
    
    if frame.shape == (settings.DISPLAY_WIDTH, settings.DISPLAY_LENGTH, settings.DISPLAY_SIZE):
        detected = detector.Detect(frame)
        
    cv2.imshow('Object detector', frame)
    if cv2.waitKey(1) == ord(settings.EXIT_KEY): break

        
video.close()
cv2.destroyAllWindows()


# In[ ]:


video.close()

