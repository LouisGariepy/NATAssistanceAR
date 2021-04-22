"""
    Author: Anthony Melin
    Date: 2019 August 14
"""
from UdpConnection import UdpConnection
import numpy as np
import cv2
import matplotlib.pyplot as plt

# # Global variables
import sys
import os
filedir = os.path.dirname(__file__) #path to this file
pcdir = os.path.join(filedir, os.pardir) #path to NATAssistanceAR/PC
sys.path.insert(1, pcdir)
import GlobalVariables.Settings as settings

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


class CameraSocket(UdpConnection):
    """
    Inherited from UdpConnection.
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

        if not self.IsConnected():
            self.echo("Request not possible: client not connected")
            return

        self.echo("Send request for data to client")
        self.sendto(b"\xff", self.client)

        if self.header:
            self.data_readable, self.data = self.recvPackets()

    def recvHeader(self):
        """
        Wait for a reader that indicate information such as number of packet that the client will send
        Return the result of FormatHeader if received the header otherwise return false
        """

        size, header = self.WaitMsg(32, 1, "header")  # wait the header

        # if received
        if size > 0:
            self.echo("Received header")
            return self.formatHeader(header)

        return False

    def recvPackets(self):
        """
        Method that receive all packets from client en gather it to restore data
        return a tuple like (data valid as boolean, data as byte array)
        """

        data = b""

        # loop as many as packet to receive
        for _ in range(self.header["packet"]):

            self.sendto(b"\xfe", self.client)  # send message for next packet
            received, packet = self.WaitMsg(65000, 1)  # wait the packet

            if not received:
                return False, self.data  # in case of timeout or error
            else:
                data += packet  # concat the packet to data

        return True, data

    def formatHeader(self, header):
        """
        Method for specify how to read the header. Return a dictionnary containing informations 
        Extract the number of packet to receive from the header.
        """

        packet = header[0]  # packet is the 1st byte received. It's implicitly converted to int
        self.echo("packet: {}".format(packet))

        return {"packet": packet}

    def getFrame(self):
        """
        Ask and return a frame. It works only with jpeg as decoder is integrated inside.
        Frame is returned as numpy array. All values are set to 0 if image is not valid. 
        """

        frame = None
        self.askData()

        # TODO: refactor try except not tested
        # try to decode frame
        try:
            frame = cv2.imdecode(np.frombuffer(self.data, np.uint8), -1)  # decode the frame

        except frame is None:
            self.ClearReception()
            frame = np.zeros((720, 1280, 3))

        return frame
