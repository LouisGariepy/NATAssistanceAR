#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2019 August 14
# -------------------------

# # Import

# In[ ]:


from CameraSocket import CameraSocket

import cv2

# # Global variables
import sys
import os
filedir = os.path.dirname(__file__) #path to this file
pcdir = os.path.join(filedir, os.pardir) #path to NATAssistanceAR/PC
sys.path.insert(1, pcdir)
import GlobalVariables.Settings as settings
# # Define host/port

# In[ ]:


_host = settings.HOST
_port = settings.CAMERA_PORT


# # Define socket and await connection

# In[ ]:


socket = CameraSocket().Bind(_host, _port)
connected = socket.WaitConnection()


# Exit if connection failed

# In[ ]:


if not connected:
    sys.exit(0)

print("Connected to {}".format(socket.client))


# # Run

# In[ ]:


while True:

    frame = socket.GetFrame()

    # display
    cv2.imshow("frame", frame)
    if cv2.waitKey(10) == ord(settings.EXIT_KEY): break

socket.Exit()
socket.close()

cv2.destroyAllWindows()


# In[ ]:


socket.Exit()
socket.close()

