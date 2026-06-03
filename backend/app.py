from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import JWT_SECRET

# ---------------- BLUEPRINTS ----------------

from routes.auth_routes import auth_bp
from routes.csv_routes import csv_bp
from routes.price_routes import price_bp
from routes.ai_routes import ai_bp
from routes.location_routes import location_bp
from routes.admin_routes import admin_bp
from routes.analytics_routes import analytics_bp
from routes.map_routes import map_bp
from routes.live_routes import live_bp

# ---------------- APP ----------------

app = Flask(__name__)

# ---------------- CONFIG ----------------

app.config["JWT_SECRET_KEY"] = JWT_SECRET

CORS(app)

jwt = JWTManager(app)

# ---------------- REGISTER BLUEPRINTS ----------------

app.register_blueprint(
    auth_bp,
    url_prefix="/api/auth"
)

app.register_blueprint(
    csv_bp,
    url_prefix="/api/csv"
)

app.register_blueprint(
    price_bp,
    url_prefix="/api/prices"
)

app.register_blueprint(
    ai_bp,
    url_prefix="/api/ai"
)

app.register_blueprint(
    location_bp,
    url_prefix="/api/location"
)

app.register_blueprint(
    admin_bp,
    url_prefix="/api/admin"
)

app.register_blueprint(
    analytics_bp,
    url_prefix="/api/analytics"
)

app.register_blueprint(
    map_bp,
    url_prefix="/api/maps"
)

app.register_blueprint(
    live_bp,
    url_prefix="/api/live"
)

# ---------------- HOME ----------------

@app.route("/")
def home():

    return jsonify({
        "app": "Farmer SaaS",
        "status": "running",
        "version": "1.0"
    })

# ---------------- DEMO PRICES ----------------

@app.route("/demo-prices")
def demo_prices():

    return jsonify([
        {
            "crop": "Tomato",
            "market": "Vijayawada",
            "price": 22
        },
        {
            "crop": "Onion",
            "market": "Guntur",
            "price": 30
        },
        {
            "crop": "Potato",
            "market": "Eluru",
            "price": 18
        }
    ])

# ---------------- ERROR HANDLERS ----------------

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "success": False,
        "message": "Route not found"
    }), 404


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500

# ---------------- START SERVER ----------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )