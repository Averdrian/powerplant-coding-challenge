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
        
        fixed_powerplants = [self._get_fixed_powerplant(powerplant) for powerplant in self.powerplants]
        fixed_powerplants.sort(key= lambda pwp: pwp.euro_mwh)
        
        total_prod = 0.0
        it = 0
        
        while total_prod < self.load:
            pwp = fixed_powerplants[it]
            
            if total_prod + pwp.pmax <= self.load:
                pwp.assigned_production = round(pwp.pmax, 2)
                
            #If the power needed is less than the minimum production, we try tu substract from the previous
            # powerplants so we satisfy the demand with the minimun in the new one
            elif total_prod + pwp.pmin > self.load:
                it_search = it - 1
                target = total_prod + pwp.pmin - self.load
                finded = False
                while not finded and it_search >= 0:
                    pwp_search = fixed_powerplants[it_search]
                    if pwp_search.assigned_production - target >= pwp_search.pmin:
                        pwp_search.assigned_production = round(pwp_search.assigned_production - target, 2)
                        total_prod -= target
                        pwp.assigned_production = round(pwp.pmin, 2)
                        finded = True
                    it_search -= 1
                    
            
            else:
                pwp.assigned_production = round(self.load - total_prod, 2)
            
            total_prod += pwp.assigned_production
            it += 1
        
        
        return [f_powerplant.to_response_json() for f_powerplant in fixed_powerplants]
    
    
    
    class _FixedPowerPlant:
        def __init__(self, name, pmin, pmax, euro_mwh, efficiency):
            self.name = name
            self.pmin = pmin
            self.pmax = pmax
            self.euro_mwh = euro_mwh
            self.efficiency = efficiency
            self.assigned_production = 0.0
            

        def to_response_json(self) -> dict:
            return {
                "name": self.name,
                "p": self.assigned_production
            }
    
    def _get_fixed_powerplant(self, powerplant: Powerplant) -> _FixedPowerPlant:
        name = powerplant.name
        euro_mwh = self._powerplant_economic_efficiency(powerplant)
        pmin = (self.fuels.wind_percentage / 100) * powerplant.pmin if powerplant.type == "windturbine" \
            else powerplant.pmin
        pmax = (self.fuels.wind_percentage / 100) * powerplant.pmax if powerplant.type == "windturbine" \
            else powerplant.pmax
        efficiency = powerplant.efficiency
        return self._FixedPowerPlant(name, pmin, pmax, euro_mwh, efficiency)
    
    
    def _powerplant_economic_efficiency(self, powerplant: Powerplant) -> float:
        if powerplant.type == "windturbine": 
            fuel_price = 0
        elif powerplant.type == "gasfired": 
            fuel_price = self.fuels.co2_euro_ton
        else: 
            fuel_price = self.fuels.kerosine_euro_mwh
            
        return fuel_price / powerplant.efficiency