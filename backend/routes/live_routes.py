from flask import Blueprint, jsonify
from services.live_price_service import update_prices_from_csv
from tasks.notification_tasks import run_price_alerts

live_bp = Blueprint("live", __name__)

# -----------------------------
# REFRESH PRICE DATA
# -----------------------------
@live_bp.route("/refresh")
def refresh():

    rows = update_prices_from_csv("data/mandi.csv")

    return jsonify({
        "success": True,
        "rows": rows
    })


# -----------------------------
# RUN PRICE ALERTS (CELERY)
# -----------------------------
@live_bp.route("/run-alerts")
def run_alerts():

    task = run_price_alerts.delay()

    return jsonify({
        "success": True,
        "task_id": task.id
    })