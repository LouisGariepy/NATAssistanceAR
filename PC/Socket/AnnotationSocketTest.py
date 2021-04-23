#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2019 August 14
# -------------------------

# # Import

# In[ ]:


from AnnotationSocket import AnnotationSocket

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


# # Define socket

# In[ ]:


socket = AnnotationSocket().Bind(_host, _port)
connected = socket.WaitConnection()


# Exit if connection failed

# In[ ]:


if not connected:
    sys.exit(0)

print("Connected to {}".format(socket.client))


# # Loop

# In[ ]:


while True:
    
    print("1 => Draw hello")
    print("2 => Clear")
    print("3 => Close connection and quit")
    choice = input()

    if choice == "1": socket.Draw("new", 0, 0, 2, "hello")
    if choice == "2": socket.Clear()
    elif choice == "3": break

socket.Exit()
socket.close()


# In[ ]:


socket.Exit()
socket.close()

