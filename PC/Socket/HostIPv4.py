import socket

# Métaclasse générique pour tous les singletons.
# Permet de sous-classer les singletons sans avoir
# besoin d'héritage multiple.
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# Intialise une variable de classe 'address' lorsque
# cette classe est créée
class HostIPv4(metaclass=Singleton):            
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        address = s.getsockname()[0]

    @staticmethod
    def getAddress():
        return HostIPv4.address


# Obtenir l'addr IPv4
if __name__ == '__main__':
    print(HostIPv4.getAddress())
