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


# # Define host/port

# In[ ]:   
hostname = socket.gethostname()   
IPAddr = socket.gethostbyname(hostname)      
print("Your Computer IP Address is:" + IPAddr)

_host = "192.168.137.1"
_port = 9999


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
    if cv2.waitKey(10) == ord('q'): break

cameraSocket.Exit()
cameraSocket.close()

cv2.destroyAllWindows()
