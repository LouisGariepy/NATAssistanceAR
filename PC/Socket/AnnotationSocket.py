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


class AnnotationSocket():
    """
    Module defining a specific socket for sending annotation command

    Inherited from UdpConnection.
    Specific socket for sending display command
    """
    udp = UdpConnection()
    
    def draw(self, cmd, *args):
        """[summary]
        Send the command and a vector to client
        Args:
            cmd ([string]): command for displaying
            args ([float]): optionnal

        """

        if not self.udp.is_connected():
            self.udp.echo("Request not possible: client not connected")
            return

        cmd += ";"

        # add each optional argument
        for arg in args:
            cmd += str(arg)+";"

        # send command and wait a message that indicate the command is applied
        self.udp.sendto(cmd.encode(), self.udp.client)
        self.udp.wait_msg(32, 1)