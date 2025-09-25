from flask import Blueprint, request, make_response


energy_production_routes = Blueprint('energy_production_routes', __name__)

@energy_production_routes.route('/productionplan', methods=['POST'])
def production_plan():
    return "Hello World"