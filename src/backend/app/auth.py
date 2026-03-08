# Login hier
from flask import Blueprint, render_template, request, redirect, url_for, flash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    return "Login Page - To be implemented"
