from . import db
from sqlalchemy import text
from flask import jsonify


class DB_Connector:
    def __init__(self):
        self.db = db

    def verify_logincode(self, logincode):
        query = db.execute(
            text("SELECT * FROM users WHERE logincode=:logincode"),
            {"logincode": logincode},
        )

        user = query.mappings().fetchone()
        if user is not None:
            return jsonify(
                {"success": True, "user_id": user[0]}
            )  # Returning the user ID
        return jsonify({"success": False})
