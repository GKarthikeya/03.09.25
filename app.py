from flask import Flask, render_template, request
from attendance_scraper import login_and_get_attendance

app = Flask(__name__)

@app.route("/")
def home():
    # Show login page
    return render_template("login.html")

@app.route("/attendance", methods=["POST"])
def attendance():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("login.html", error="Please enter both username and password")

    result = login_and_get_attendance(username, password)

    if not result["overall"]["success"]:
        return render_template("login.html", error="Login failed. Check credentials.")

    return render_template("attendance.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
