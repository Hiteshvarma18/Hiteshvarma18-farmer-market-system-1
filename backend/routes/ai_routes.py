from flask import Blueprint, request, jsonify
from ai_model.predict import predict_price

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/predict")
def predict():

    crop = request.args.get("crop")
    market = request.args.get("market")
    days = int(request.args.get("days", 0))

    if not crop or not market:
        return jsonify({
            "success": False,
            "message": "crop and market required"
        }), 400

    price = predict_price(crop, market, days)

    return jsonify({
        "crop": crop,
        "market": market,
        "future_days": days,
        "predicted_price": round(price, 2)
    })