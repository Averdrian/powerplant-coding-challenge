from energy_production.domain.models.fuels import Fuels
from energy_production.domain.models.powerplant import Powerplant
from energy_production.domain.services.production_plan_service import ProductionPlanService

class CalculateProductionPlan:
    
    load : int
    fuels : Fuels
    powerplants : list[Powerplant]
    
    def __init__(self, load : int, fuels: Fuels, powerplants : list[Powerplant]):
        self.load = load
        self.fuels = fuels
        self.powerplants = powerplants
        
    def execute(self) -> dict:
        
        production_plan = ProductionPlanService.calculate_production_plan(self.load, self.fuels, self.powerplants)
        return production_plan
        