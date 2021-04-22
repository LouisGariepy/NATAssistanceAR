"""
    Author: Anthony Melin
    Date: 2019 August 14
"""

# @package AnnotationSocket

# for importation from outside this directory
from UdpConnection import UdpConnection

"""
###############################################################
#                     AnnotationSocket                        #
#                                                             #
#  Draw(self, cmd, vector, *args)                             #
#                                                             #
###############################################################
"""


class AnnotationSocket(UdpConnection):

    """
    Module defining a specific socket for sending annotation command

    Inherited from UdpConnection.
    Specific socket for sending display command
    """

    def Draw(self, cmd, *args):
        """[summary]
        Send the command and a vector to client
        Args:
            cmd ([string]): command for displaying
            args ([float]): optionnal

        """

        if not self.IsConnected():
            self.echo("Request not possible: client not connected")
            return

        message = cmd + ";"

        # add each optional argument
        for arg in args:
            message += str(arg)+";"

        # send command and wait a message that indicate the command is applied
        self.sendto(message.encode(), self.client)
        self.WaitMsg(32, 1)
