# DB Models

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logincode = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    options = db.Column(db.Text, nullable=True)  # JSON string of user options


class selection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    selection_json = db.Column(db.Text, nullable=False)
    finalized = db.Column(db.Boolean, default=False, nullable=False)
