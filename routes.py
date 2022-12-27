from flask import render_template, redirect, request
from init import app, user
from database import *


@app.route("/")
def welcome_page():
    if user.is_auth:
        return redirect("/feed")
    return render_template("welcome.html")


@app.route("/auth", methods=["GET"])
def auth_page():
    if user.is_auth:
        return redirect("/feed")
    return render_template("auth.html")


@app.route("/register", methods=["GET"])
def register_page():
    if user.is_auth:
        return redirect("/feed")
    return render_template("register.html")


@app.route("/report", methods=["GET"])
def report_page():
    if not user.is_auth:
        return redirect("/")
    return render_template("report.html", user=user)


@app.route("/report-check", methods=["GET"])
def report_check_page():
    if not user.is_auth:
        return redirect("/")
    return render_template("report-check.html", user=user)


@app.route("/cabinet")
def cabinet_page():
    if not user.is_auth:
        return redirect("/")
    return render_template("cabinet.html", user=user)


@app.route("/feed")
def feed_page():
    if not user.is_auth:
        return redirect("/")
    return render_template("feed.html", user=user)


@app.route("/auth", methods=["POST"])
def check_auth_page():
    user.is_auth = user.try_auth(request.form["login"], request.form["password"])
    return redirect("/feed")


@app.route("/register", methods=["POST"])
def do_register_page():
    user.is_auth = True
    return redirect("/feed")


@app.route("/report", methods=["POST"])
def do_report_page():
    if not user.is_auth:
        return redirect("/")
    user.add_report(
        request.form["title"],
        request.form["description"],
        request.form["location"],
        request.form["files"] if "files" in request.form else ""
    )
    return redirect("/feed")


@app.route("/checked", methods=["GET"])
def set_checked_report_page():
    if not user.is_auth:
        return redirect("/")
    user.set_checked(request.values["id"])
    return redirect("/feed")