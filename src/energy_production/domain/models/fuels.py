class Fuels:
    
    gas_euro_mwh : float
    kerosine_euro_mwh : float
    co2_euro_ton : int
    wind_percentage : int
    
    def __init__(self, gas_euro_mwh, kerosine_euro_mwh, co2_euro_ton, wind_percentage):
        self.gas_euro_mwh = gas_euro_mwh
        self.kerosine_euro_mwh = kerosine_euro_mwh
        self.co2_euro_ton = co2_euro_ton
        self.wind_percentage = wind_percentage
        
    
    @classmethod
    def from_dict(cls, fuels_dict: dict) -> "Fuels":
        return cls(
            fuels_dict["gas(euro/MWh)"],
            fuels_dict["kerosine(euro/MWh)"],
            fuels_dict["co2(euro/ton)"],
            fuels_dict["wind(%)"]
        )
        