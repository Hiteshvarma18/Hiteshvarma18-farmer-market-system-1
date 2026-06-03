from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from db import get_db

from utils.validators import valid_phone, strong_password
from utils.security import hash_password, verify_password

from services.otp_service import (
    generate_otp,
    verify_otp,
    can_resend
)

auth_bp = Blueprint("auth", __name__)

# ----------------------------------
# SEND OTP
# ----------------------------------

@auth_bp.route("/send-otp", methods=["POST"])
def send_otp_route():

    data = request.get_json()

    phone = data.get("phone", "").strip()

    if not valid_phone(phone):
        return jsonify({
            "success": False,
            "message": "Invalid phone number"
        }), 400

    if not can_resend(phone):
        return jsonify({
            "success": False,
            "message": "Wait 60 seconds before requesting another OTP"
        }), 429

    otp = generate_otp(phone)

    # TODO:
    # Integrate Fast2SMS here

    print("OTP:", otp)

    return jsonify({
        "success": True,
        "message": "OTP sent successfully"
    })


# ----------------------------------
# VERIFY OTP
# ----------------------------------

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp_route():

    data = request.get_json()

    phone = data.get("phone", "")
    otp = data.get("otp", "")

    if verify_otp(phone, otp):

        return jsonify({
            "success": True,
            "message": "OTP verified"
        })

    return jsonify({
        "success": False,
        "message": "Invalid or expired OTP"
    }), 400


# ----------------------------------
# SIGNUP
# ----------------------------------

@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    user_id = data.get("user_id", "").strip()
    phone = data.get("phone", "").strip()
    password = data.get("password", "")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "User ID required"
        }), 400

    if not valid_phone(phone):
        return jsonify({
            "success": False,
            "message": "Invalid phone number"
        }), 400

    if not strong_password(password):
        return jsonify({
            "success": False,
            "message": "Weak password"
        }), 400

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT id FROM users WHERE phone=%s",
        (phone,)
    )

    if cur.fetchone():

        cur.close()
        db.close()

        return jsonify({
            "success": False,
            "message": "Phone already registered"
        }), 400

    hashed = hash_password(password)

    cur.execute("""
        INSERT INTO users
        (
            user_id,
            phone,
            password,
            is_verified
        )
        VALUES
        (%s,%s,%s,%s)
    """, (
        user_id,
        phone,
        hashed,
        True
    ))

    db.commit()

    cur.close()
    db.close()

    return jsonify({
        "success": True,
        "message": "Account created"
    })


# ----------------------------------
# LOGIN
# ----------------------------------

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    phone = data.get("phone", "").strip()
    password = data.get("password", "")

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "SELECT * FROM users WHERE phone=%s",
        (phone,)
    )

    user = cur.fetchone()

    cur.close()
    db.close()

    if not user:

        return jsonify({
            "success": False,
            "message": "Phone number not found"
        }), 404

    if not verify_password(
        password,
        user["password"]
    ):

        return jsonify({
            "success": False,
            "message": "Incorrect password"
        }), 401

    token = create_access_token(
        identity=str(user["id"])
    )

    return jsonify({
        "success": True,
        "token": token,
        "user_id": user["user_id"]
    })


# ----------------------------------
# FORGOT PASSWORD
# ----------------------------------

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()

    phone = data.get("phone", "")

    if not valid_phone(phone):

        return jsonify({
            "success": False,
            "message": "Invalid phone number"
        }), 400

    otp = generate_otp(phone)

    print("RESET OTP:", otp)

    return jsonify({
        "success": True,
        "message": "Reset OTP sent"
    })


# ----------------------------------
# RESET PASSWORD
# ----------------------------------

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json()

    phone = data.get("phone")
    otp = data.get("otp")
    password = data.get("password")

    if not verify_otp(phone, otp):

        return jsonify({
            "success": False,
            "message": "Invalid OTP"
        }), 400

    if not strong_password(password):

        return jsonify({
            "success": False,
            "message": "Weak password"
        }), 400

    hashed = hash_password(password)

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        UPDATE users
        SET password=%s
        WHERE phone=%s
    """, (
        hashed,
        phone
    ))

    db.commit()

    cur.close()
    db.close()

    return jsonify({
        "success": True,
        "message": "Password updated"
    })