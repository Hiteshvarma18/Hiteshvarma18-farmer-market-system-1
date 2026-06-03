from flask import Blueprint
from flask import jsonify

from db import get_db

map_bp = Blueprint(
    "map",
    __name__
)

@map_bp.route("/mandis")
def mandis():

    db = get_db()

    cursor = db.cursor(
        dictionary=True
    )

    cursor.execute("""
    SELECT *
    FROM mandi_locations
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)