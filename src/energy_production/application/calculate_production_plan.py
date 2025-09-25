from energy_production.domain.models.fuels import Fuels
from energy_production.domain.models.powerplant import Powerplant

class CalculateProductionPlan:
    
    load : int
    fuels : Fuels
    powerplants : list[Powerplant]
    
    def __init__(self, load : int, fuels: Fuels, powerplants : list[Powerplant]):
        self.load = load
        self.fuels = fuels
        self.powerplants = powerplants
        
    def execute(self) -> str:
        pass