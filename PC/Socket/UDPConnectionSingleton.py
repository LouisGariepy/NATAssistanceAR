import UdpConnection


class UDPConnectionSingleton:
    __instance = None

    @staticmethod
    def getUDPConnectionInstance():
        if UDPConnectionSingleton.__instance is None:
            UDPConnectionSingleton()
        return UDPConnectionSingleton.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if UDPConnectionSingleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            UDPConnectionSingleton.__instance = UdpConnection
