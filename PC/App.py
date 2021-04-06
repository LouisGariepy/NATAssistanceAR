#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2019 August 14
# -------------------------

# # Import

# In[ ]:


from Socket.CameraSocket import CameraSocket
from Socket.RayCollisionSocket import RayCollisionSocket
from Socket.AnnotationSocket import AnnotationSocket

from Tensorflow.ObjectDetection import *
from Tensorflow.ObjectDetector import ObjectDetector

from Scenario.SimpleObjectDetection import SimpleObjectDetection
from Scenario.SimpleNAT import *

import cv2
import sys
import numpy as np

# # Global variables
import GlobalVariables.Settings as settings


# In[ ]:


# scenario = SimpleObjectDetection()
# scenario = SimpleNATReleaseTimer()
scenario = SimpleNATRelease()


# # Object detection configuration

# ### Load model

# In[ ]:


category_index = load_categories(settings.LABELS, settings.NUM_CLASSES)
sess, inputs, outputs = load_model(settings.GRAPH)


# ### Set frame detector

# In[ ]:


detector = ObjectDetector(sess, inputs, outputs, category_index)
detector.SetThreshold(settings.DETECTOR_THRESHOLD)
detector.draw = True


# # Define sockets and await connection
# 
# ### Camera
# 
# Exit if connection failed

# In[ ]:


cameraSocket = CameraSocket().Bind(settings.HOST, settings.CAMERA_PORT)
connected = cameraSocket.WaitConnection()    

print(settings.HOST + " " + str(settings.CAMERA_PORT))
      
if not connected:
    cameraSocket.close()
    sys.exit(0)
else:
	print("Camera socket connected")


# ### Ray collision
# 
# Exit if connection failed

# In[ ]:


collisionSocket = RayCollisionSocket().Bind(settings.HOST, settings.COLLISION_PORT)
print(settings.HOST + " " + str(settings.COLLISION_PORT))
connected = collisionSocket.WaitConnection()
if not connected:
    cameraSocket.close()
    collisionSocket.close()
    sys.exit(0)
else:
	print("Collision socket connected")
	
# ### Annotation
# 
# Exit if connection failed

# In[ ]:


annotationSocket = AnnotationSocket().Bind(settings.HOST, settings.ANNOTATION_PORT)
print(settings.HOST + " " + str(settings.ANNOTATION_PORT))
connected = annotationSocket.WaitConnection()
if not connected:
    cameraSocket.close()
    collisionSocket.close()
    annotationSocket.close()
    sys.exit(0)
else:
	print("Annotation socket connected")

# # Loop

# In[ ]:


while True:

    # frame
    frame = cameraSocket.GetFrame()
    
    # detection
    detected = detector.Detect(frame)

    # ray collision test
    positions = collisionSocket.AskPositions(detected["centers"])
    
    # annotation
    if len(positions) > 0 and len(positions) == len(detected["centers"]):
        detected["positions"] = positions
        scenario.Update(detected, annotationSocket)
    
    # display
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord(settings.EXIT_KEY): break


cameraSocket.Exit()
collisionSocket.Exit()
annotationSocket.Exit()

cameraSocket.close()
collisionSocket.close()
annotationSocket.close()

cv2.destroyAllWindows()


# In[ ]:


cameraSocket.close()
collisionSocket.close()
annotationSocket.close()


# In[ ]:


scenario.obj

