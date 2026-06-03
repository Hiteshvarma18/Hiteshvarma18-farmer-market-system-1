from flask import Blueprint
from flask import jsonify
from flask import request

from services.location_service import (
    get_markets,
    get_market_prices
)

location_bp = Blueprint(
    "location",
    __name__
)

@location_bp.route("/markets")
def markets():

    return jsonify(
        get_markets()
    )


@location_bp.route("/prices")
def prices():

    market = request.args.get(
        "market"
    )

    return jsonify(
        get_market_prices(
            market
        )
    )