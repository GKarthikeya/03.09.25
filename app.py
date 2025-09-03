# app.py

from flask import Flask, render_template, request, redirect, url_for
from attendance_scraper import login_and_get_attendance

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/attendance", methods=["POST"])
def attendance():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("login.html", error="Please enter username and password.")

    # Get attendance using scraper
    data = login_and_get_attendance(username, password)

    # If login failed or scraper returned error
    if not data["overall"]["success"]:
        return render_template("login.html", error=data["overall"].get("message", "Login failed."))

    # Prepare subject data for table
    subjects = data["subjects"]
    table_data = []
    for i, (code, sub) in enumerate(subjects.items(), start=1):
        table_data.append({
            "sno": i,
            "code": code,
            "name": sub["name"],
            "present": sub["present"],
            "absent": sub["absent"],
            "percentage": sub["percentage"],
            "status": sub["status"]
        })

    return render_template("attendance.html", table_data=table_data, overall=data["overall"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
