from . import Abs_Factory
from . import Contexte as cont

class ContexteFactory(Abs_Factory):
    def __init__(self) -> None :
        pass
    def build_strategy(self):
        return cont.Contexte()