"""
    Author: Anthony Melin
    Date: 2019 August 14
"""
import cv2
import numpy as np
from pandas import np

import GlobalVariables.Settings as settings
from UDPConnectionSingleton import UDPConnectionSingleton

"""
###############################################################
# Module defining a specific socket for receive frames        #
#                                                             #
#                     UdpCameraSocket                         #
#  AskData(self)                                              #
#  RecvHeader(self)                                           #
#  RecvPackets(self)                                          #
#  FormatHeader(self, header)                                 #
#  GetFrame(self)                                             #
#                                                             #
###############################################################
"""


class CameraSocket():
    UDPConnectionSingleton = UDPConnectionSingleton.getUDPConnectionInstance()
    """
    Udp server for asking data in byte format to connected client.
    Receive frames as data and make sure it's readable
    """

    def __init__(self):
        super().__init__()
        self.data = b""
        self.data_readable = False
        self.header = self.recvHeader()

    def askData(self):
        """
        Request data to the client.
        data_readable indicate if received data are valid. If so, it's stored in data
        """

        if not self.UDPConnectionSingleton.IsConnected():
            self.UDPConnectionSingleton.echo("Request not possible: client not connected")
            return

        self.UDPConnectionSingleton.echo("Send request for data to client")
        self.UDPConnectionSingleton.sendto(b"\xff", self.UDPConnectionSingleton.client)

        if self.header:
            self.data_readable, self.data = self.recvPackets()

    def recvHeader(self):
        """
        Wait for a reader that indicate information such as number of packet that the client will send
        Return the result of FormatHeader if received the header otherwise return false
        """

        size, header = self.UDPConnectionSingleton.WaitMsg(32, 1, "header")  # wait the header
        
        # wait the header
        size, header = self.WaitMsg(32, 1, "header")  

        # if received
        if size > 0:
            self.UDPConnectionSingleton.echo("Received header")
            return self.UDPConnectionSingleton.formatHeader(header)

        return False

    def recvPackets(self):
        """
        Method that receive all packets from client en gather it to restore data
        return a tuple like (data valid as boolean, data as byte array)
        """

        data = b""

        # loop as many as packet to receive
        for _ in range(self.header["packet"]):
            
            # send message for next packet
            self.sendto(b"\xfe", self.client) 
             
            # wait the packet
            received, packet = self.WaitMsg(settings.SOCKET_BUFSIZE, 1)  

            self.UDPConnectionSingleton.sendto(b"\xfe", self.UDPConnectionSingleton.client)  # send message for next packet
            received, packet = self.UDPConnectionSingleton.WaitMsg(settings.SOCKET_BUFSIZE, 1)  # wait the packet
            self.UDPConnectionSingleton.sendto(b"\xfe",
                                               self.UDPConnectionSingleton.client)  # send message for next packet
            received, packet = self.UDPConnectionSingleton.WaitMsg(settings.SOCKET_BUFSIZE, 1)  # wait the packet

            if not received:
                return False, self.data  
            
            # concat the packet to data
            data += packet  

        return True, data

    def formatHeader(self, header):
        """
        Method for specify how to read the header. Return a dictionnary containing informations 
        Extract the number of packet to receive from the header.
        """

        # packet is the 1st byte received. It's implicitly converted to int
        packet = header[0]
        self.echo("packet: {}".format(packet))
        packet = header[0]  # packet is the 1st byte received. It's implicitly converted to int
        self.UDPConnectionSingleton.echo("packet: {}".format(packet))

        return {"packet": packet}

    def getFrame(self):
        """
        Ask and return a frame. It works only with jpeg as decoder is integrated inside.
        Frame is returned as numpy array. All values are set to 0 if image is not valid. 
        """

        frame = None
        self.askData()

        # try to decode frame
        try:
            # decode the frame
            frame = cv2.imdecode(np.frombuffer(
                self.data, np.uint8), -1)  

        except:
            self.ClearReception()
            frame = np.zeros((settings.DISPLAY_WIDTH
                            , settings.DISPLAY_LENGTH
                            , settings.DISPLAY_SIZE))

        return frame
