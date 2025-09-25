from flask import Blueprint, request, make_response
from energy_production.application.calculate_production_plan import CalculateProductionPlan
from energy_production.domain.models.fuels import Fuels
from energy_production.domain.models.powerplant import Powerplant

energy_production_routes = Blueprint('energy_production_routes', __name__)

@energy_production_routes.route('/productionplan', methods=['POST'])
def production_plan():
    payload = request.json
    
    load = payload['load']
    fuels = Fuels.from_dict(payload['fuels'])
    powerplants = [ Powerplant.from_dict(powerplant_dict) for powerplant_dict in payload['powerplants'] ]
    
    prod_plan = CalculateProductionPlan(load, fuels, powerplants).execute()
    
    if len(prod_plan) > 0: 
        response = make_response(prod_plan, 200)
    else: 
        response = make_response({'error': "There is no production plan possible with given parameters"}, 422)
    
    return response