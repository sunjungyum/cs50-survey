import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # Check for all possible empty fields
    if not request.form.get("first-name"):
        return render_template("error.html", error="first name")
    elif not request.form.get("last-name"):
        return render_template("error.html", error="last name")
    elif (request.form.get("grade") == ""):
        return render_template("error.html", error="grade")
    elif request.form.get("meal") == "none":
        return render_template("error.html", error="favorite meal")

    # Post entry into survey.csv
    with open("survey.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["first-name", "last-name", "grade", "meal"])
        writer.writerow({"first-name": request.form.get("first-name"),
                         "last-name": request.form.get("last-name"),
                         "grade": request.form.get("grade"),
                         "meal": request.form.get("meal")})
    return redirect('/sheet')


@app.route("/sheet", methods=["GET"])
# Read survey.csv to create a table in sheet.html
def get_sheet():
    with open("survey.csv", "r") as file:
        reader = csv.reader(file)
        entries = list(reader)
    return render_template("sheet.html", entries=entries)