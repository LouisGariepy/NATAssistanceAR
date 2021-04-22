from . import Abs_Factory as f
from . import Contexte2D as cont

class ContexteFactory2D(f.Abs_Factory):
    def __init__(self) -> None :
        pass
    def build_strategy(self):
        return cont.Contexte2D()