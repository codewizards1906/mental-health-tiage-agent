from flask import Flask, render_template_string, request
import csv
from datetime import datetime

app = Flask(__name__)


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
        "LOW": ["Exercise", "Sleep well", "Relaxation"],
        "MODERATE": ["Talk to friends", "Stress control", "Counseling"],
        "HIGH": ["Consult doctor", "Avoid isolation", "Therapy"],
        "EMERGENCY": ["Call helpline", "Immediate help", "Contact family"]
    }
    return data[level]


def log(score, level):
    with open("triage_results.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), score, level])


html = """
<h2>Mental Health Triage Agent</h2>

<form method="post">

{% for q in questions %}
<p>{{q}}</p>
<select name="q{{loop.index}}">
<option value="0">0</option>
<option value="1">1</option>
<option value="2">2</option>
<option value="3">3</option>
</select>
{% endfor %}

<br><br>
<input type="submit">

</form>

{% if result %}
<h3>Score: {{score}}</h3>
<h3>Level: {{level}}</h3>
<h3>Severity: {{sev}}</h3>

<ul>
{% for t in tips %}
<li>{{t}}</li>
{% endfor %}
</ul>

{% endif %}
"""


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        score = 0

        for i in range(1, 10):
            score += int(request.form["q" + str(i)])

        level = classify(score)
        sev = severity(score)
        t = tips(level)

        log(score, level)

        return render_template_string(
            html,
            questions=questions,
            result=True,
            score=score,
            level=level,
            sev=sev,
            tips=t
        )

    return render_template_string(
        html,
        questions=questions,
        result=False
    )


if __name__ == "__main__":
    app.run(debug=True)