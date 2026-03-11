from . import db
from sqlalchemy import text
from flask import jsonify

from .models import User


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

    def retrieve_user_options(self, user_id):
        query = db.execute(
            text("SELECT options FROM users WHERE id=:user_id"),
            {"user_id": user_id},
        )
        result = query.mappings().fetchone()
        if result is not None:
            return jsonify({"success": True, "options": result[0]})
        return jsonify({"success": False, "options": None})

    def add_user_to_db(self, user: User):
        db.add(user)
        db.commit()
        return jsonify({"success": True, "user_id": user.id})

    def get_user_selection(self, user_id):
        query = db.execute(
            text("SELECT selection FROM users WHERE id=:user_id"),
            {"user_id": user_id},
        )
        result = query.mappings().fetchone()
        if result is not None:
            return jsonify({"success": True, "selection": result[0]})
        return jsonify({"success": False, "selection": None})
