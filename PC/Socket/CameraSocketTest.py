#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2019 August 14
# -------------------------

# # Import

# In[ ]:


from CameraSocket import CameraSocket
import socket
import sys
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
hostname = socket.gethostname()   
IPAddr = socket.gethostbyname(hostname)      
print("Your Computer IP Address is:" + IPAddr)

_host = settings.HOST
_port = settings.CAMERA_PORT


# # Define socket and await connection

# In[ ]:


cameraSocket = CameraSocket().Bind(_host, _port)
connected = cameraSocket.WaitConnection()


# Exit if connection failed

# In[ ]:


if not connected:
    sys.exit(0)

print("Connected to {}".format(cameraSocket.client))


# # Run

# In[ ]:

while True:

    frame = cameraSocket.getFrame()

    # display
    cv2.imshow("frame", frame)
    if cv2.waitKey(10) == ord(settings.EXIT_KEY): break

cameraSocket.Exit()
cameraSocket.close()

cv2.destroyAllWindows()
