class Powerplant:
    
    name : str
    type: str
    efficiency : float
    pmin: int
    pmax : int
    
    
    def __init__(self, name, type, efficiency, pmin, pmax):
        self.name = name
        self.type = type
        self.efficiency = efficiency
        self.pmin = pmin
        self.pmax = pmax
    
    
    @classmethod
    def from_dict(cls, powerplant_dict : dict) -> "Powerplant":
        return cls(
            powerplant_dict['name'],
            powerplant_dict['type'],
            powerplant_dict['efficiency'],
            powerplant_dict['pmin'],
            powerplant_dict['pmax']
        )