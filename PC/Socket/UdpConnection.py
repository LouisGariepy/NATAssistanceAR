"""
    Author: Anthony Melin
    Date: 2019 August 14
"""

import socket
# # Global variables
import sys
import os
filedir = os.path.dirname(__file__)  # path to this file
pcdir = os.path.join(filedir, os.pardir)  # path to NATAssistanceAR/PC
sys.path.insert(1, pcdir)

import GlobalVariables.Settings as settings
from Utils import ipv4_decode
from UDPConnectionSingleton import Singleton

"""
###############################################################
#                           UdpSocket                         #
#                                                             #
#  __init__(self)                                             #
#  Online(self, host, port)                                   #
#  ClearReception(self)                                       #
#  WaitMsg(self, size, timeout=0, message="")                 #
#  WaitConnection(self, timeout=10)                           #
#  IsConnectionEnabled(self)                                  #
#  EnableEcho(self)                                           #
#  DisableEcho(self)                                          #
#  Exit(self)                                                 #
#                                                             #
###############################################################
"""
    

## Base Udp socket with methods for client connection.
# The remote connection is called "client"
# Informations could be displayed in console, use EchoEnabled.
class UdpConnection(socket.socket, metaclass=Singleton):
    
    host = settings.HOST
    port = settings.CAMERA_PORT
    client = None
    echo = lambda x, y: None

    """###########################################################"""

    ## Constructor that build the socket object
    def __init__(self):

        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM)
        self.echo("Socket created")

    """###########################################################"""

    ## Bind the socket to an adress
    # @param host string, the IP adress to bind
    # @param port int, the port to bind
    # return itself for allowing shorter syntax used in some example scripts
    def Bind(self, host, port):

        if type(host) != str: "host argument type must be str"
        if type(port) != int: "port argument type must be int"

        self.host = host
        self.port = port

        self.bind((self.host, self.port))
        self.echo("Socket bind to {}:{}".format(host, port))
        return self

    """###########################################################"""

    ## This method is a way to clear the reception buffer. It avoid to read an obsolet message
    def ClearReception(self):

        try:
            self.settimeout(0.01)
            self.recv(settings.SOCKET_BUFSIZE)

        except socket.timeout:
            pass

        else:
            self.ClearReception()

    """###########################################################"""

    ## Wait for a specifed time a message from the client
    # Return a tuple like (message length, message), (0,0) when message is not received
    # @param size int, the buffer size for receive the message, should be greater than message otherwise Datagram error is raised
    # @param timeout float, time to wait in second. If none is specified, wait until message is received
    # @param type_message string, appear in console information when specified
    def WaitMsg(self, size, timeout=0, type_message=""):

        if type(timeout) != int:  "timeout argument type must be int"
        if type(type_message) != str: "type_message argument type must be str"

        if timeout: self.settimeout(timeout)
        self.echo("Awaiting message ({})...".format(type_message))
        try:
            msg = self.recv(size)
            return len(msg), msg

        except socket.timeout:
            self.echo("Timeout for message awaiting ({}sec)".format(timeout))
            return 0, 0

        except OSError:
            self.echo("Datagram error")
            return 0, 0

    """###########################################################"""

    ## Wait a client connection. Return true if connection is made
    # @param timeout float, time to wait in second, default : 10sec
    def WaitConnection(self, timeout=10):

        if type(timeout) != int:  "timeout argument type must be int"

        # await a connect sequence from client
        self.echo("Awaiting connection...")
        try:
            self.settimeout(timeout)
            msg = self.recv(6)

        except socket.timeout:
            self.echo("Timeout for connection awaiting")
            return False

        except OSError:
            self.ClearReception()
            self.echo("Datagram error")
            return False

        else:
            # unzip informations
            self.client_addr = ipv4_decode(msg[:4])
            self.client_port = int.from_bytes(msg[4:], "big")
            self.client = (self.client_addr, self.client_port)

            # send a byte for connection confirmation
            self.sendto(b"\xff", self.client)
            self.ClearReception()

            self.echo("Connection from {}".format(self.client))
            return True

    """###########################################################"""

    ## Indicate if a client is connected
    # Return a boolean, true : client connected
    def IsConnected(self):

        if self.client:
            return True
        else:
            return False

    """###########################################################"""

    ## Allow the socket to display informations in the console
    def EnableEcho(self):

        self.echo = lambda x: print(x)

    """###########################################################"""

    ## Disable console informations
    def DisableEcho(self):

        self.echo = lambda x: None

    """###########################################################"""

    ## Send a byte that indicate an end of connection and delete client adress
    def Exit(self):

        if self.IsConnected():
            self.sendto(b"\x01", self.client)
            self.client = False
