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


# # Global variables
import sys
import os
filedir = os.path.dirname(__file__) #path to this file
pcdir = os.path.join(filedir, os.pardir) #path to NATAssistanceAR/PC
sys.path.insert(1, pcdir)
import GlobalVariables.Settings as settings

# # Load model and its labelmap

# In[ ]:


category_index = load_categories(settings.LABELS, settings.NUM_CLASSES)
sess, inputs, outputs = load_model(settings.GRAPH)


# # Run

# In[ ]:


import cv2
import numpy as np

video = cv2.VideoCapture(0)
if not video.isOpened(): raise BaseException("Camera not found")

while(True):

    ret, frame = video.read()
    frame_expanded = np.expand_dims(frame, axis=0)
    (boxes, scores, classes, num) = sess.run(outputs, feed_dict={inputs: frame_expanded})
    draw_bounding_boxes(frame, boxes, classes, scores, category_index, 0.65, 4)

    cv2.imshow('Object detector', frame)
    if cv2.waitKey(1) == ord(settings.EXIT_KEY): break

video.release()
cv2.destroyAllWindows()

