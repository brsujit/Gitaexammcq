from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = "exam_secret_key"

PASSWORD = "gitaexam"  # password for students

# Load questions
with open("questions.json", "r") as f:
    questions = json.load(f)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        name = request.form.get("name")
        if password == PASSWORD:
            session["user"] = name
            return redirect(url_for("exam"))
        else:
            return render_template("login.html", error="Wrong password! Try again.")
    return render_template("login.html")

@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        score = 0
        for i, q in enumerate(questions):
            if request.form.get(f"q{i}") == q["answer"]:
                score += 1
        session["score"] = score
        return redirect(url_for("result"))

    return render_template("exam.html", questions=questions, name=session["user"])

@app.route("/result")
def result():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("result.html", name=session["user"], score=session["score"], total=len(questions))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
