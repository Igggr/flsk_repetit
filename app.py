from flask import Flask, render_template
import json

app = Flask(__name__)
app.config.from_object('config')

with open("json_data/teachers.json", "r") as f:
    teachers = json.load(f)
with open("json_data/goals.json", "r") as f:
    goals = json.load(f)


@app.route("/")
def index():
    return render_template("index.html", teachers=teachers)


@app.route("/goals/<goal>/")
def goal_view(goal):
    return render_template("goal.html", goal=goal, goals=goals,
                           teachers=teachers)


@app.route("/profiles/<int:teacher_id>/")
def profile(teacher_id):
    return render_template("profile.html", id=teacher_id, teachers=teachers)


@app.route('/request/')
def request_view():
    return render_template('pick.html')


@app.route('/booking/<int:id>/')
def booking(id):
    return render_template("booking.html", id=id)


@app.template_filter()
def teachers_for_goal(teachers, goal):
    return filter(lambda teacher: goal in teacher['goals'], teachers)


@app.context_processor
def utility_processor():
    def is_free(teacher, day, hour):
        return teacher['free'][day][hour]
    return dict(is_free=is_free)


if __name__ == "__main__":
    app.run()
