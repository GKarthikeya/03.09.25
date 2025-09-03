from flask import Flask, render_template, request
from attendance_scraper import login_and_get_attendance

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/attendance", methods=["POST"])
def attendance():
    try:
        username = request.form["username"]
        password = request.form["password"]

        result = login_and_get_attendance(username, password)

        if not result["overall"]["success"]:
            return render_template("attendance.html", overall=result["overall"], table_html="<p>Error: Login failed</p>")

        # Build table HTML
        table_html = "<table><tr><th>Code</th><th>Subject</th><th>Present</th><th>Absent</th><th>%</th><th>Status</th></tr>"
        for code, sub in result["subjects"].items():
            table_html += f"<tr><td>{code}</td><td>{sub['name']}</td><td>{sub['present']}</td><td>{sub['absent']}</td><td>{sub['percentage']}%</td><td>{sub['status']}</td></tr>"
        table_html += "</table>"

        return render_template("attendance.html", overall=result["overall"], table_html=table_html)

    except Exception as e:
        return f"<h2>500 Error</h2><p>{str(e)}</p>", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
