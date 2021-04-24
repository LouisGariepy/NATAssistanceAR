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


class UdpConnection(socket.socket, metaclass=Singleton):
    """
    Base Udp socket with methods for client connection.
    The remote connection is called "client"
    Informations could be displayed in console, use EchoEnabled.
    """
    host = settings.HOST
    port = settings.CAMERA_PORT
    client = None
    echo = lambda x, y: None

    def __init__(self):

        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM)
        self.echo("Socket created")

    def bind(self, host, port):
        """
        Bind the socket to an adress and a port.
        return itself for allowing shorter syntax used in some example scripts
        """

        assert type(host) == str, "host argument type must be str"
        assert type(port) == int, "port argument type must be int"

        self.host = host
        self.port = port

        self.bind((self.host, self.port))
        self.echo("Socket bind to {}:{}".format(host, port))
        return self

    def clear_reception(self):
        """
        This method is a way to clear the reception buffer. It avoid to read an obsolet message.
        """

        try:
            self.settimeout(0.01)
            self.recv(settings.SOCKET_BUFSIZE)
            
        except socket.timeout:
            pass

        else:
            self.clear_reception()

    def wait_msg(self, size, timeout=0, type_message=""):
        """
        Wait for a specifed time a message from the client.
        Return a tuple like (message length, message), (0,0) when message is not received
        """

        assert type(timeout) == int, "timeout argument type must be int"
        assert type(type_message) == str, "type_message argument type must be str"

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

    def wait_connection(self, timeout=10):
        """
        Wait a client connection. Return true if connection is made.
        """

        assert type(timeout) == int, "timeout argument type must be int"

        # await a connect sequence from client
        self.echo("Awaiting connection...")
        try:
            self.settimeout(timeout)
            msg = self.recv(6)

        except socket.timeout:
            self.echo("Timeout for connection awaiting")
            return False

        except OSError:
            self.clear_reception()
            self.echo("Datagram error")
            return False

        else:
            # unzip informations
            self.client_addr = ipv4_decode(msg[:4])
            self.client_port = int.from_bytes(msg[4:], "big")
            self.client = (self.client_addr, self.client_port)

            # send a byte for connection confirmation
            self.sendto(b"\xff", self.client)
            self.clear_reception()

            self.echo("Connection from {}".format(self.client))
            return True

    def is_connected(self):
        """
        Indicate if a client is connected.
        """

        if self.client:
            return True
        else:
            return False

    def enable_echo(self):
        """
        Allow the socket to display informations in the console.
        """

        self.echo = lambda x: print(x)

    def disable_echo(self):
        """
        Disable console informations.
        """

        self.echo = lambda x: None

    def exit(self):
        """
        Send a byte that indicate an end of connection and delete client adress.
        """

        if self.is_connected():
            self.sendto(b"\x01", self.client)
            self.client = False
