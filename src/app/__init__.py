from flask import Flask
from flask import render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import secrets

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # TODO: Load environment variables from .env file
    app.config["SECRET_KEY"] = secrets.token_hex(32)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kwgost.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from .views import views
        from .auth import auth

        app.register_blueprint(views)
        app.register_blueprint(auth)

        db.create_all()

    return app
