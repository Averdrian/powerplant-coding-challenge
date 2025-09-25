from energy_production.domain.models.fuels import Fuels
from energy_production.domain.models.powerplant import Powerplant

class ProductionPlanService:
    
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
    
    @staticmethod
    def calculate_production_plan(load: int, fuels: Fuels, powerplants : list[Powerplant]) -> str:
        
        fixed_powerplants = [ProductionPlanService._get_fixed_powerplant(powerplant, fuels) for powerplant in powerplants]
        fixed_powerplants.sort(key= lambda pwp: pwp.euro_mwh)
        
        total_prod = 0.0
        it = 0
        
        while total_prod < load and it < len(fixed_powerplants):
            pwp = fixed_powerplants[it]
            
            if total_prod + pwp.pmax <= load:
                pwp.assigned_production = round(pwp.pmax, 2)
                
            #If the power needed is less than the minimum production, we try tu substract from the previous
            # powerplants so we satisfy the demand with the minimun in the new one
            elif total_prod + pwp.pmin > load:
                powerplants_backup = fixed_powerplants.copy()
                
                it_search = it - 1
                target = total_prod + pwp.pmin - load
                finded = False
                
                while not finded and it_search >= 0:
                    pwp_search = fixed_powerplants[it_search]
                    #If we can substract the remaining from the next powerplant we do and finish the iterations
                    if pwp_search.assigned_production - target >= pwp_search.pmin:
                        pwp_search.assigned_production = round(pwp_search.assigned_production - target, 2)
                        total_prod -= target
                        pwp.assigned_production = round(pwp.pmin, 2)
                        finded = True
                    #If not, we substract all we can and iterate to next powerplant
                    else:
                        
                        total_prod -= (pwp_search.assigned_production - pwp_search.pmin)
                        target -= (pwp_search.assigned_production - pwp_search.pmin)
                        pwp_search.assigned_production = round(pwp_search.pmin, 2)
                    it_search -= 1
                #If we were not able to substract and equilibrate without overflowing, we assume
                # this powerplant is not part of the solution and we recover the production calculated before substracting
                if not finded:
                    fixed_powerplants = powerplants_backup        
            
            else:
                pwp.assigned_production = round(load - total_prod, 2)
            
            total_prod += pwp.assigned_production
            it += 1
        
        
        return [f_powerplant.to_response_json() for f_powerplant in fixed_powerplants] if total_prod == load else []
    
    
    
    
    @staticmethod
    def _get_fixed_powerplant(powerplant: Powerplant, fuels: Fuels) -> _FixedPowerPlant:
        name = powerplant.name
        euro_mwh = ProductionPlanService._powerplant_economic_efficiency(powerplant, fuels)
        pmin = (fuels.wind_percentage / 100) * powerplant.pmin if powerplant.type == "windturbine" \
            else powerplant.pmin
        pmax = (fuels.wind_percentage / 100) * powerplant.pmax if powerplant.type == "windturbine" \
            else powerplant.pmax
        efficiency = powerplant.efficiency
        return ProductionPlanService._FixedPowerPlant(name, pmin, pmax, euro_mwh, efficiency)
    
    
    @staticmethod
    def _powerplant_economic_efficiency(powerplant: Powerplant, fuels: Fuels) -> float:
        if powerplant.type == "windturbine": 
            fuel_price = 0
        elif powerplant.type == "gasfired": 
            fuel_price = fuels.co2_euro_ton
        else: 
            fuel_price = fuels.kerosine_euro_mwh
            
        return fuel_price / powerplant.efficiency