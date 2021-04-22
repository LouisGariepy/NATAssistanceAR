from Scenario.Strategy import Base

class Contexte:
    def __init__(self):
        self.strategy = Base.BaseScenario()

    def set_strategy(self, other):
        self.strategy = other