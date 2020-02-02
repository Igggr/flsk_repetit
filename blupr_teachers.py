from flask import render_template, request, Blueprint
from forms import NamePhoneForm, RequestMatchingTeacherForm
import json
import datetime


blp = Blueprint('blp', __name__)

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


def is_free_at_the_time(teacher, day, hour):
    return teacher['free'][day][hour]


def availiable_now(teacher):
    week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    now = datetime.datetime.today()
    day = week[now.weekday()]
    hour = f"{ now.hour // 2 * 2}:00"

    return is_free_at_the_time(teacher, day, hour)


@blp.route("/")         # покажет доступных сейчас учителей
def index():
    free_teachers = [t for t in teachers if availiable_now(t)]
    free_teachers.sort(key=lambda t: t['rating'])

    return render_template("index.html",
                           teachers=free_teachers[:6])


@blp.route("/all/")     # покажет всех учителей
def index_all():
    teachers.sort(key=lambda t: t['rating'])
    return render_template("all.html", teachers=teachers[:6])


@blp.route("/goals/<goal>/")
def goal_view(goal):
    goal_teachers = [t for t in teachers if goal in t['goals']]
    return render_template("goal.html", goal=goal, goals=goals,
                           teachers=goal_teachers)


@blp.route("/profiles/<int:teacher_id>/")
def profile(teacher_id):
    return render_template("profile.html",
                           id=teacher_id,
                           teacher=teachers[teacher_id])


@blp.route('/booking/<int:id>/<string:day>/<string:hour>/')
def booking(id, day, hour):
    form = NamePhoneForm()
    return render_template("booking.html",
                           teacher=teachers[id],
                           time={"day": day, "hour": hour},
                           days=days,
                           form=form
                           )


@blp.route("/booking_done/", methods=["POST"])
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


@blp.route('/request/', methods=["GET"])
def request_view():
    form = RequestMatchingTeacherForm()
    return render_template('request.html', goals=goals, form=form)


@blp.route("/request_done/", methods=["POST"])
def request_done():
    goal = request.form.get('goal', 'travel')
    time = request.form.get('time', '1-2')
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


@blp.context_processor
def utility_processor():
    return dict(is_free=is_free_at_the_time)
