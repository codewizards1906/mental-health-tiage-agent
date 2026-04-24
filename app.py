from flask import Flask, render_template_string, request
import csv
from datetime import datetime
import threading
import time
import os

app = Flask(__name__)

# ---------------- QUESTIONS ----------------
questions = [
    "Little interest or pleasure in doing things",
    "Feeling down, depressed, or hopeless",
    "Trouble falling or staying asleep",
    "Feeling tired or having little energy",
    "Poor appetite or overeating",
    "Feeling bad about yourself",
    "Trouble concentrating",
    "Feeling nervous or anxious",
    "Thoughts of self-harm"
]

# ---------------- LOGIC ----------------
def classify(score):
    if score >= 21:
        return "EMERGENCY"
    elif score >= 14:
        return "HIGH"
    elif score >= 7:
        return "MODERATE"
    else:
        return "LOW"


def severity(score):
    if score >= 21:
        return "Severe"
    elif score >= 14:
        return "Moderately Severe"
    elif score >= 7:
        return "Moderate"
    else:
        return "Mild"


def tips(level):
    data = {
        "LOW": ["Exercise regularly", "Maintain good sleep", "Relaxation"],
        "MODERATE": ["Talk to friends", "Stress management", "Counseling"],
        "HIGH": ["Consult doctor", "Avoid isolation", "Therapy"],
        "EMERGENCY": ["Call helpline", "Immediate help", "Contact family"]
    }
    return data[level]

# ---------------- EMERGENCY CONTACTS ----------------
def emergency_contacts():
    return {
        "helplines": [
            ("Kiran Mental Health Helpline", "1800-599-0019"),
            ("AASRA Suicide Prevention", "9820466726"),
            ("Police", "100"),
            ("Ambulance", "102")
        ],
        "hospitals": [
            ("Mukut Hospital, Sector 34 Chandigarh", "0172-2678901"),
            ("Sohana Hospital, Mohali", "0172-2212345")
        ],
        "psychologists": [
            ("Dr. Mehta (Psychologist)", "9876501234"),
            ("Dr. Sharma (Counsellor)", "9812349876"),
            ("Mind Care Clinic", "9876541122")
        ],
        "personal": [
            ("Rahul (Friend)", "9812345678"),
            ("Aman (Friend)", "9876543210")
        ]
    }

# ---------------- MAP LINK ----------------
def hospital_map_link():
    return "https://www.google.com/maps/search/hospitals+near+me"

# ---------------- LOGGER ----------------
def log(score, level):
    with open("triage_results.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), score, level])

# ---------------- HTML ----------------
html = """
<!DOCTYPE html>
<html>
<head>
<title>Mental Health Triage Agent</title>
<style>
body { font-family: Arial; margin: 40px; }
h2 { color: #2c3e50; }
h3 { margin-top: 20px; }
.emergency { color: red; }
</style>
</head>

<body>

<h2>🧠 Mental Health Triage Agent</h2>

<form method="post">

{% for q in questions %}
<p>{{q}}</p>
<select name="q{{loop.index}}">
<option value="0">0 - Not at all</option>
<option value="1">1 - Several days</option>
<option value="2">2 - More than half the days</option>
<option value="3">3 - Nearly every day</option>
</select>
{% endfor %}

<br><br>
<input type="submit" value="Submit Assessment">

</form>

{% if result %}

<h3>📊 Score: {{score}}</h3>
<h3>🚦 Level: {{level}}</h3>
<h3>📌 Severity: {{sev}}</h3>

<h3>💡 Tips</h3>
<ul>
{% for t in tips %}
<li>{{t}}</li>
{% endfor %}
</ul>

{% if level == "HIGH" or level == "EMERGENCY" %}

<h3 class="emergency">🚨 Emergency Support</h3>

<h4>📞 Helplines</h4>
<ul>
{% for name, number in contacts.helplines %}
<li>{{name}} - <a href="tel:{{number}}">{{number}}</a></li>
{% endfor %}
</ul>

<h4>🏥 Hospitals</h4>
<ul>
{% for name, number in contacts.hospitals %}
<li>{{name}} - <a href="tel:{{number}}">{{number}}</a></li>
{% endfor %}
</ul>

<h4>🧠 Psychologists & Counsellors</h4>
<ul>
{% for name, number in contacts.psychologists %}
<li>{{name}} - <a href="tel:{{number}}">{{number}}</a></li>
{% endfor %}
</ul>

<h4>👨‍👩‍👧 Personal Contacts</h4>
<ul>
{% for name, number in contacts.personal %}
<li>{{name}} - <a href="tel:{{number}}">{{number}}</a></li>
{% endfor %}
</ul>

<h4>📍 Nearby Hospitals</h4>
<a href="{{map_link}}" target="_blank">Open in Google Maps</a>

{% endif %}

{% endif %}

</body>
</html>
"""

# ---------------- ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        score = 0
        for i in range(1, 10):
            score += int(request.form["q" + str(i)])

        level = classify(score)
        sev = severity(score)
        t = tips(level)

        contacts = {}
        map_link = ""

        if level == "HIGH" or level == "EMERGENCY":
            contacts = emergency_contacts()
            map_link = hospital_map_link()

        log(score, level)

        return render_template_string(
            html,
            questions=questions,
            result=True,
            score=score,
            level=level,
            sev=sev,
            tips=t,
            contacts=contacts,
            map_link=map_link
        )

    return render_template_string(html, questions=questions, result=False)

# ---------------- AUTO OPEN BROWSER ----------------
def open_browser():
    time.sleep(2)
    os.system("start chrome http://127.0.0.1:5000")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    app.run(debug=True)