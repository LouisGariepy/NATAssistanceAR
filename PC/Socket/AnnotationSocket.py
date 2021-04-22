"""
    Author: Anthony Melin
    Date: 2019 August 14
"""

from UDPConnectionSingleton import UDPConnectionSingleton

"""
###############################################################
#                     AnnotationSocket                        #
#                                                             #
#  Draw(self, cmd, vector, *args)                             #
#                                                             #
###############################################################
"""


class AnnotationSocket():
    UDPConnectionSingleton = UDPConnectionSingleton.getUDPConnectionInstance()
    """
    Module defining a specific socket for sending annotation command
    Specific socket for sending display command
    """

    def Draw(self, cmd, *args):
        """[summary]
        Send the command and a vector to client
        Args:
            cmd ([string]): command for displaying
            args ([float]): optionnal

        """

        if not self.UDPConnectionSingleton.IsConnected():
            self.UDPConnectionSingleton.echo("Request not possible: client not connected")
            return

        message = cmd + ";"

        # add each optional argument
        for arg in args:
            message += str(arg)+";"

        # send command and wait a message that indicate the command is applied
        self.UDPConnectionSingleton.sendto(cmd.encode(), self.UDPConnectionSingleton.client)
        self.UDPConnectionSingleton.WaitMsg(32, 1)
