from flask import Blueprint, jsonify, request
from db import get_db

analytics_bp = Blueprint("analytics", __name__)

# -------------------------------
# CHART DATA API (NEW)
# -------------------------------
@analytics_bp.route("/chart-data")
def chart_data():

    crop = request.args.get("crop", "Tomato")
    market = request.args.get("market", "Vijayawada")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT date, price
        FROM crop_prices
        WHERE crop=%s AND market=%s
        ORDER BY date ASC
        LIMIT 50
    """, (crop, market))

    rows = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify({
        "crop": crop,
        "market": market,
        "data": rows
    })