from flask import Blueprint
from flask import request
from flask import jsonify

from services.csv_service import import_csv

csv_bp = Blueprint(
    "csv",
    __name__
)

@csv_bp.route(
    "/upload-csv",
    methods=["POST"]
)
def upload_csv():

    if "file" not in request.files:

        return jsonify({
            "success":False,
            "message":"No file uploaded"
        })

    file = request.files["file"]

    rows = import_csv(file)

    return jsonify({
        "success":True,
        "rows_imported":rows
    })