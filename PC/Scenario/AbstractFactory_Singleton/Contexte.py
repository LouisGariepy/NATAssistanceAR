import BaseScenario

class Contexte:
    def __init__(self):
        self.strategy = BaseScenario()

    def set_strategy(self, other):
        self.strategy = other