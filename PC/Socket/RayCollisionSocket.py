"""
    Author: Anthony Melin
    Date: 2019 August 14
"""

## @package RayCollisionSocket
# Module defining a specific socket for ray hit test

# coding: utf-8

# # Import
# # Global variables
import sys
import os
filedir = os.path.dirname(__file__) #path to this file
pcdir = os.path.join(filedir, os.pardir) #path to NATAssistanceAR/PC
sys.path.insert(1, pcdir)

# for importation from here
from UdpConnection import UdpConnection
import GlobalVariables.Settings as settings
import numpy as np

"""
####################################################################
#                      UdpRayCollisionSocket                       #
#                                                                  #
#  AskPositions(self, coords)                                      #
#  Format(self, coords)                                            #
#  Unzip(self, packet)                                             #
#                                                                  #
####################################################################
"""

class RayCollisionSocket():
    """
    Inherited from UdpConnection. Socket for receiving 3D coordinates 
    coresponding to 2D coordinates sended previously
    """
    udp = UdpConnection()

    def ask_positions(self, coords):
        """[summary]
        
        Request to the client the associated coordinates in space of the 2D coordinates.
        
        Args:
            coords ([list]): a list of 2D coordinates type (x, y) with 
                            normalised values coresponding to the client camera view.
            
        Returns:
            [list]: a list of coordinates type (x, y, z) with 
                    values exprimed in meters or an empty list if no reply is received.
        """
        
        # if not connected or  if coords list is empty
        if not self.udp.is_connected() or len(coords) == 0:
            self.udp.echo("Request not possible: client not connected")
            return []
        
        # convert list to message
        message = self.ToBytes(coords) 
        
        # send the 2D coordinates
        self.udp.sendto(message, self.udp.client)
        self.udp.echo("Send request for positions to client")
        
        # await coordinates
        received, packet = self.udp.wait_msg(settings.SOCKET_BUFSIZE, 1)
        
        # convert packet (string) to list if received
        if received > 0:
            return self.ToArray(packet)
        
        return []
            
    def ToBytes(self, coords):
        """[summary]
        
        Convert the 2D coordinates list to a string for being sendable
        
        Args:
            coords ([list]): list of 2D coordinates like [(x1,y1), (x2,y2), (x3,y3), ... ]

        Returns:
            [bytes]: returns a string as byte array like x1,y1;x2,y2;x3,y3;... 
        """        
        
        message = ""
        
        # for each coordinates, concat to the message x and y value
        for x, y in coords:
            message += "{},{};".format(x,y)
        
        #remove the last character (a useless ;) and convert to bytes
        message = message[:-1].encode() 
        
        return message
    
    def ToArray(self, packet):
        """[summary]
        Convert the received message to 3D coordinate list
        
        Args:
            packet ([bytes]): bytes received from client, format : x1,y1,z1;x2,y2,z2;x3,y3,z3;

        Returns:
            [array]: an array like [ (x1,y1,z1), (x2,y2,z2), (x3,y3,z3), ... ] 
        """
        
        # convert bytes to string and remove last character (a useless ;)
        packet = packet.decode()[:-1] 
        packet = packet.split(";")
        
        # foreach vector as single string, split into 3 values (x, y, z)
        for n, vec in enumerate(packet):
            packet[n] = vec.split(",")
        
        packet = np.asarray(packet).astype(float)
          
        return packet