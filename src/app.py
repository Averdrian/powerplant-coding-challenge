from flask import Flask
from energy_production.infrastructure.api import energy_production_routes

app = Flask(__name__)

app.register_blueprint(energy_production_routes)

if __name__ == "__main__":
    app.run(debug=True, port=8888)