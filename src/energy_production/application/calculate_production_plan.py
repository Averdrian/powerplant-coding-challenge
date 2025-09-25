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
        # ordered_powerplants_by_efficiency = self._ordered_powerplants_by_economic_efficiency()
        
        fixed_powerplants = [self._get_fixed_powerplant(powerplant) for powerplant in self.powerplants]
        fixed_powerplants.sort(key= lambda pwp: pwp.euro_mwh)
        print([pwp.to_json() for pwp in fixed_powerplants])
        
        satiesfied_load = 0
        solution = []
        it = 0
        
        
        return "aa"
    
    
    
    class _FixedPowerPlant:
        def __init__(self, name, pmin, pmax, euro_mwh):
            self.name = name
            self.pmin = pmin
            self.pmax = pmax
            self.euro_mwh = euro_mwh
            
        def to_json(self):
            return {
                "name": self.name,
                "pmin": self.pmin,
                "pmax": self.pmax,
                "euro_mwh" : self.euro_mwh
            }
    
    def _get_fixed_powerplant(self, powerplant: Powerplant) -> _FixedPowerPlant:
        name = powerplant.name
        euro_mwh = self._powerplant_economic_efficiency(powerplant)
        pmin = self.fuels.wind_percentage * powerplant.pmin if powerplant.type == "windturbin" \
            else powerplant.pmin * powerplant.efficiency
        pmax = self.fuels.wind_percentage * powerplant.pmax if powerplant.type == "windturbin" \
            else powerplant.pmax * powerplant.efficiency
        return self._FixedPowerPlant(name, pmin, pmax, euro_mwh)
        
         
        
    
    # def _ordered_powerplants_by_economic_efficiency(self) -> list[Powerplant]:
    #     return sorted(self.powerplants, key=self._powerplant_economic_efficiency)
    
    
    def _powerplant_economic_efficiency(self, powerplant: Powerplant) -> float:
        if powerplant.type == "windturbine": 
            fuel_price = 0
        elif powerplant.type == "gasfired": 
            fuel_price = self.fuels.co2_euro_ton
        else: 
            fuel_price = self.fuels.kerosine_euro_mwh
            
        return fuel_price / powerplant.efficiency
    

        