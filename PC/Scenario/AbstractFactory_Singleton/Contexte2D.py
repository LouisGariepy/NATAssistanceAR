from Scenario.Strategy import Base2D

class Contexte2D:
    def __init__(self):
        self.strategy2D = Base2D.BaseScenario2D()

    def set_strategy2D(self, other):
        self.strategy2D = other