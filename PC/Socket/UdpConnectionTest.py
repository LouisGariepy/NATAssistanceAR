#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2019 August 14
# -------------------------

# # Imports

# In[ ]:


from UdpConnection import UdpConnection

# # Global variables
import sys
import os
filedir = os.path.dirname(__file__) #path to this file
pcdir = os.path.join(filedir, os.pardir) #path to NATAssistanceAR/PC
sys.path.insert(1, pcdir)
import GlobalVariables.Settings as settings


# # Host and Port definition

# In[ ]:


HOST = settings.HOST
PORT = settings.CAMERA_PORT


# # Socket declaration

# In[ ]:


socket = UdpConnection()
socket.Bind(HOST, PORT)

# Shorter syntax is possible
# connection = UdpConnection().Bind(HOST, PORT)


# The following line allow to display informations

# In[ ]:


socket.EchoEnabled()


# # Socket connection

# In[ ]:


connected = socket.WaitConnection(20) # await a connection message for 20sec

if not connected:
    print("Connection failed")
    sys.exit(0) # stop the program

print("Connected to {}".format(socket.client))


# # Send message

# In[ ]:


message = b"\xff"

socket.sendto(message, socket.client)


# # Receive message

# In[ ]:


size, message = socket.WaitMsg(4096, 20, "test")

if size:
    print("Received message ({}) : {}".format(size, message))


# # Close socket

# In[ ]:


socket.Exit()
socket.close()

