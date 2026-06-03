from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from db import get_db
from utils.security import verify_password

from tasks.price_tasks import refresh_prices
from tasks.ai_tasks import retrain_ai


admin_bp = Blueprint("admin", __name__)

# ==============================
# ADMIN LOGIN
# ==============================
@admin_bp.route("/login", methods=["POST"])
def admin_login():

    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Missing credentials"
        }), 400

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM admins WHERE username=%s",
        (username,)
    )

    admin = cursor.fetchone()

    cursor.close()
    db.close()

    if not admin:
        return jsonify({
            "success": False,
            "message": "Admin not found"
        }), 404

    if not verify_password(password, admin["password"]):
        return jsonify({
            "success": False,
            "message": "Wrong password"
        }), 401

    token = create_access_token(identity=str(admin["id"]))

    return jsonify({
        "success": True,
        "token": token
    })


# ==============================
# USERS LIST
# ==============================
@admin_bp.route("/users", methods=["GET"])
def users():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, user_id, phone, created_at
        FROM users
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)


# ==============================
# CROP PRICES LIST
# ==============================
@admin_bp.route("/prices", methods=["GET"])
def prices():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM crop_prices
        ORDER BY date DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)


# ==============================
# ADD PRICE
# ==============================
@admin_bp.route("/add-price", methods=["POST"])
def add_price():

    data = request.get_json() or {}

    required = ["crop", "market", "price", "date"]

    if not all(k in data for k in required):
        return jsonify({
            "success": False,
            "message": "Missing fields"
        }), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO crop_prices (crop, market, price, date)
        VALUES (%s, %s, %s, %s)
    """, (
        data["crop"],
        data["market"],
        data["price"],
        data["date"]
    ))

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "success": True,
        "message": "Price added"
    })


# ==============================
# DELETE PRICE
# ==============================
@admin_bp.route("/delete-price/<int:price_id>", methods=["DELETE"])
def delete_price(price_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM crop_prices WHERE id=%s",
        (price_id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "success": True,
        "message": "Price deleted"
    })


# ==============================
# ANALYTICS
# ==============================
@admin_bp.route("/analytics", methods=["GET"])
def analytics():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    users = cursor.fetchone()["total_users"]

    cursor.execute("SELECT COUNT(*) AS total_prices FROM crop_prices")
    prices = cursor.fetchone()["total_prices"]

    cursor.execute("SELECT AVG(price) AS avg_price FROM crop_prices")
    avg_price = cursor.fetchone()["avg_price"] or 0

    cursor.close()
    db.close()

    return jsonify({
        "total_users": users,
        "total_prices": prices,
        "average_price": round(avg_price, 2)
    })


# ==============================
# CELERY: REFRESH PRICES
# ==============================
@admin_bp.route("/refresh-prices", methods=["POST"])
def refresh_prices_now():

    task = refresh_prices.delay()

    return jsonify({
        "success": True,
        "task_id": task.id
    })


# ==============================
# CELERY: RETRAIN AI
# ==============================
@admin_bp.route("/retrain-ai", methods=["POST"])
def retrain_model():

    task = retrain_ai.delay()

    return jsonify({
        "success": True,
        "task_id": task.id
    })