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
NUM_CLASSES = 99


# # Import module

# In[ ]:


from ObjectDetection import *


# # Load model and its labelmap

# In[ ]:


category_index = load_categories(LABELS, NUM_CLASSES)
sess, inputs, outputs = load_model(GRAPH)


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
    if cv2.waitKey(1) == ord('q'): break

video.release()
cv2.destroyAllWindows()

