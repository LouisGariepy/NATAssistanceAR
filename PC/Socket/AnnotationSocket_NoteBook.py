#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2019 August 14
# -------------------------

# # Import

# In[ ]:


from AnnotationSocket import AnnotationSocket

import sys


# # Define host/port

# In[ ]:


_host = "192.168.137.1"
_port = 9999


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

