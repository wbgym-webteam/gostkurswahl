from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
)

views = Blueprint("views", __name__, static_folder="static")


@views.route("/")
def root():
    return redirect(url_for("auth.login"))


@views.route("/selection")
def selection():
    return "selection"
