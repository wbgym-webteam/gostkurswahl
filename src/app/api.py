from flask import jsonify, request, Blueprint
from db_connector import DB_Connector as dbc

api = Blueprint("api", __name__)


# Login
@api.route("/login", methods=["POST"])
def api_login():
    data = request.get_json()
    logincode = data.get("logincode")
    verification = dbc.verify_logincode(logincode)
    if dbc.verify_logincode(logincode) is not None:
        return jsonify(
            {"success": True, "user_id": verification.get_json().get("user_id")}
        )
    return jsonify({"success": False})
