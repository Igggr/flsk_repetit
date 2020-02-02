from flask import Flask, render_template, request
import json
import datetime

from forms import NamePhoneForm, RequestMatchingTeacherForm

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "secret"

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
week = [day for day in days]


@app.route("/")
def index():
    return render_template("index.html", teachers=teachers)


@app.route("/all/")
def index_all():
    return render_template("all.html", teachers=teachers)


@app.route("/goals/<goal>/")
def goal_view(goal):
    return render_template("goal.html", goal=goal, goals=goals,
                           teachers=teachers)


@app.route("/profiles/<int:teacher_id>/")
def profile(teacher_id):
    return render_template("profile.html", id=teacher_id, teachers=teachers)


@app.route('/request/', methods=["GET"])
def request_view():
    form = RequestMatchingTeacherForm()
    return render_template('request.html', goals=goals, form=form)


@app.route('/booking/<int:id>/<string:day>/<string:hour>/')
def booking(id, day, hour):
    form = NamePhoneForm()
    return render_template("booking.html",
                           teacher=teachers[id],
                           time={"day": day, "hour": hour},
                           days=days,
                           form=form
                           )


@app.route("/booking_done/", methods=["POST"])
def booking_done():
    name = request.form["name"]
    phone = request.form["phone"]
    day = request.form["day"]
    hour = request.form["hour"]
    teacher_id = request.form["teacher_id"]

    with open('json_data/booking.json', "r") as f:
        bookings = json.load(f)

    bookings.append({"student_name": name, "student_phone": phone,
                     "day": day, "hour": hour, "teacher_id": teacher_id})

    with open('json_data/booking.json', "w") as f:
        json.dump(bookings, f)

    return render_template("done.html",
                           title={"label": "Тема", "value": "Пробный урок"},
                           time={"label": days[day], "value": f"{hour}:00"},
                           name=name,
                           phone=phone)


@app.template_filter()
def teachers_for_goal(teachers, goal):
    return filter(lambda teacher: goal in teacher['goals'], teachers)


@app.template_filter()
def availiable_now(teachers):
    now = datetime.datetime.today()
    day = week[now.weekday()]
    hour = f"{ now.hour // 2 * 2}:00"

    def is_free(teacher):
        return teacher["free"][day][hour]

    return [teacher for teacher in teachers if is_free(teacher)]


@app.context_processor
def utility_processor():
    def is_free(teacher, day, hour):
        return teacher['free'][day][hour]
    return dict(is_free=is_free)


@app.route("/echo/", methods=["POST"])
def request_done():
    goal = request.form['goal']
    time = request.form['time']
    name = request.form['name']
    phone = request.form['phone']

    with open("json_data/request.json", "r") as f:
        lesson_requests = json.load(f)

    lesson_requests.append({"student_name": name, "student_phone": phone,
                            "goal": goal, "time": time})

    with open("json_data/request.json", "w") as f:
        json.dump(lesson_requests, f)

    return render_template(
        'done.html',
        title={"label": "Цель занятий", "value": goals[goal]},
        time={"label": "Времени есть", "value": f"{time} часа в неделю"},
        name=name,
        phone=phone
    )


if __name__ == "__main__":
    app.run()
