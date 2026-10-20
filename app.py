import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = "birthdays.db"


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Add the user's entry into the database
        name = request.form.get("name")
        day = request.form.get("day")
        month = request.form.get("month")

        if not name or not day or not month:
            return redirect("/")

        #convert the date and month to integers
        try:
            day = int(day)
            month = int(month)
        except ValueError:
            flash("Day and Month must be integers")
            return redirect("/")
        
        try:
            with sqlite3.connect(db) as conn:
                conn.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", (name, day, month))
                conn.commit()

        except sqlite3.Error as e:
            flash("Error inseting the data in the database", e)

        return redirect("/")

    else:

        # Display the entries in the database on index.html
        with sqlite3.connect(db) as conn:
            conn.row_factory = sqlite3.Row
            birthdays = conn.execute("SELECT * FROM birthdays").fetchall()
            print(birthdays)
        return render_template("index.html", birthdays=birthdays)

@app.route("/delete/<int:birthday_id>", methods=["POST"])
def delete_user(birthday_id):
    try:
        with sqlite3.connect(db) as conn:
            conn.execute("DELETE FROM birthdays WHERE id = ?", (birthday_id,))
            conn.commit()
    except sqlite3.OperationalError as e:
        flash("Server error", e)
    return redirect("/")



