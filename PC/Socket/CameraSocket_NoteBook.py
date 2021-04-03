#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2019 August 14
# -------------------------

# # Import

# In[ ]:


from CameraSocket import CameraSocket

import sys
import cv2


# # Define host/port

# In[ ]:


_host = "192.168.137.1"
_port = 9999


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
    if cv2.waitKey(10) == ord('q'): break

socket.Exit()
socket.close()

cv2.destroyAllWindows()


# In[ ]:


socket.Exit()
socket.close()

