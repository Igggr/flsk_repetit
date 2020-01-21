from flask import Flask, render_template
from data import teachers, goals

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", teachers=teachers)


@app.route("/goals/<goal>/")
def goal_view(goal):
    return render_template("goal.html", goal=goal, goals=goals,
                           teachers=teachers)


@app.route("/profiles/<int:id>/")
def profile(teacher_id):
    return render_template("profile.html", id=teacher_id)


@app.route('/request/')
def request_view():
    return render_template('pick.html')


@app.route('/booking/<int:id>/')
def booking(id):
    return render_template("booking.html", id=id)


if __name__ == "__main__":
    app.run()
