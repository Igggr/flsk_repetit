from flask import Flask, render_template, request
import json

app = Flask(__name__)
app.config.from_object('config')

with open("json_data/teachers.json", "r") as f:
    teachers = json.load(f)
with open("json_data/goals.json", "r") as f:
    goals = json.load(f)

days = {"mon": "Понедельник",
        "tue": "Вторник",
        "wed": "Среда",
        "thu": "Четверг",
        "fri": "Пятница",
        "sat": "Суббота",
        "sun": "Воскресенье"}


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
    return render_template('request.html', goals=goals)


@app.route('/booking/<int:id>/<string:day>/<string:hour>/')
def booking(id, day, hour):
    return render_template("booking.html",
                           teacher=teachers[id],
                           time={"day": day, "hour": hour},
                           days=days)


@app.route("/booking_done/", methods=["POST"])
def booking_done():
    name = request.form["clientName"]
    phone = request.form["clientPhone"]
    day = request.form["day"]
    hour = request.form["hour"]
    return render_template("done.html",
                           title={"label": "Тема", "value": "Пробный урок"},
                           time={"label": days[day], "value": f"{hour}:00"},
                           name=name,
                           phone=phone)


@app.template_filter()
def teachers_for_goal(teachers, goal):
    return filter(lambda teacher: goal in teacher['goals'], teachers)


@app.context_processor
def utility_processor():
    def is_free(teacher, day, hour):
        return teacher['free'][day][hour]
    return dict(is_free=is_free)


@app.route("/echo", methods=["POST"])
def handle_request():
    goal = request.form['goal']
    time = request.form['time']
    name = request.form['name']
    phone = request.form['phone']
    return render_template(
        'done.html',
        title={"label": "Цель занятий", "value": goals[goal]},
        time={"label": "Времени есть", "value": f"{time} часа в неделю"},
        name=name,
        phone=phone
    )


if __name__ == "__main__":
    app.run()
