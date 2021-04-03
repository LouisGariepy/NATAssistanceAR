#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2019 August 14
# -------------------------

# # Global variables

# In[ ]:


MODEL_DIRECTORY = "MODEL_DIRECTORY"

GRAPH = MODEL_DIRECTORY + "/frozen_inference_graph.pb"
LABELS = MODEL_DIRECTORY + "/labelmap.pbtxt"
NUM_CLASSES = 1000


# # Import module

# In[ ]:


from ObjectDetection import *
from ObjectDetector import ObjectDetector


# # Load model

# In[ ]:


category_index = load_categories(LABELS, NUM_CLASSES)
sess, inputs, outputs = load_model(GRAPH)


# # Set frame detector

# In[ ]:


detector = ObjectDetector(sess, inputs, outputs, category_index)
detector.SetThreshold(60)
detector.draw = True


# # Loop

# In[ ]:


import cv2
import numpy as np

frame = cv2.resize(cv2.imread("im.jpg"), (1280, 720))

detected = detector.Detect(frame)

cv2.imshow('Object detector', frame)
cv2.waitKey(0)

cv2.destroyAllWindows()


# In[ ]:


import cv2
import numpy as np
import time

from RemoteCam import RemoteCam


video = RemoteCam(10000, 3)

while(True):

    frame = video.getFrame()
    
    if frame.shape == (720, 1280, 3):
        detected = detector.Detect(frame)
        
    cv2.imshow('Object detector', frame)
    if cv2.waitKey(1) == ord('q'): break

        
video.close()
cv2.destroyAllWindows()


# In[ ]:


video.close()

