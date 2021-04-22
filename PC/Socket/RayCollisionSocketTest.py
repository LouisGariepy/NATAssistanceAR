#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2019 August 14
# -------------------------

# # Import
# # Global variables
import sys
import os
filedir = os.path.dirname(__file__) #path to this file
pcdir = os.path.join(filedir, os.pardir) #path to NATAssistanceAR/PC
sys.path.insert(1, pcdir)
import GlobalVariables.Settings as settings
# In[ ]:


from RayCollisionSocket import RayCollisionSocket

import cv2
import numpy as np
import sys


# # Built-in methods test

# In[ ]:


socket = RayCollisionSocket()

# kind of array to send
vec2 = np.asarray([
    (0.5,0.5),
    (0,0)
])
print("message built :", socket.ToBytes(vec2), "\n")

# kind of received message
vec3 = b"0.5,0.5,0.5;0,0,0;"
print("message converted :", socket.ToArray(vec3))


# # Server
# 
# ### Define host/port 

# In[ ]:


_host = settings.HOST
_port = settings.CAMERA_PORT


# ### Define coordinates to send

# In[ ]:


_coords = np.asarray([(0.5,0.5)]) # center


# ### Start server and wait connection

# In[ ]:


socket = RayCollisionSocket().Bind(_host, _port)
connected = socket.WaitConnection()


# Exit if connection failed

# In[ ]:


if not connected:
    sys.exit(0)

print("Connected to {}".format(socket.client))


# # Loops
# ## Manual

# In[ ]:


while True:
        
    print("1 => Ask position")
    print("2 => Close connection and quit")
    choice = input()

    if choice == "1":
        positions = socket.AskPositions(_coords)
        if len(positions) > 0: # control that coordinates are valid
            print("received :", positions)

    elif choice == "2": break

socket.Exit()
socket.close()


# ## Graphical

# In[ ]:


while True:

    frame = np.zeros((200, 800)).astype(float)
    
    # ray collision test
    positions = socket.AskPositions(_coords)
    
    # display
    if len(positions) > 0:
        vec = positions[0].astype(str)
        text = "x={} y={} z={}".format(vec[0],vec[1],vec[2])
        cv2.putText(frame, text, (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord(settings.EXIT_KEY): break


socket.Exit()
socket.close()

cv2.destroyAllWindows()


# In[ ]:


socket.Exit()
socket.close()

