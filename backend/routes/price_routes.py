from flask import Blueprint
from flask import jsonify

from db import get_db

price_bp = Blueprint(
    "price",
    __name__
)

@price_bp.route("/latest")
def latest_prices():

    db = get_db()

    cursor = db.cursor(
        dictionary=True
    )

    cursor.execute("""
    SELECT
        crop,
        market,
        price,
        date
    FROM crop_prices
    ORDER BY date DESC
    LIMIT 100
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)