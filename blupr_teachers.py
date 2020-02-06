from flask import render_template, request, Blueprint
from forms import NamePhoneForm, RequestMatchingTeacherForm
import json
import datetime
from models import db, Teacher, Goal, RequestLesson, Booking

blp = Blueprint('blp', __name__)

days = {"mon": "Понедельник",
        "tue": "Вторник",
        "wed": "Среда",
        "thu": "Четверг",
        "sun": "Воскресенье",
        "fri": "Пятница",
        "sat": "Суббота",
        }


def is_free_at_the_time(teacher, day, hour):
    return json.loads(teacher.shedule)[day][hour]


def availiable_now(teacher):
    week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    now = datetime.datetime.today()
    day = week[now.weekday()]
    hour = f"{ now.hour // 2 * 2}:00"

    return is_free_at_the_time(teacher, day, hour)


@blp.route("/")         # покажет доступных сейчас учителей
def index():
    teachers = Teacher.query.order_by(Teacher.rating.desc()).limit(6)

    return render_template("index.html",
                           teachers=teachers)


@blp.route("/all/")     # покажет всех учителей
def index_all():
    teachers = Teacher.query.order_by(Teacher.rating.desc()).limit(6)
    return render_template("all.html", teachers=teachers)


@blp.route("/goals/<goal>/")
def goal_view(goal):
    goal = Goal.query.filter_by(title=goal).one()
    return render_template("goal.html", goal=goal,
                           teachers=goal.teachers)


@blp.route("/profiles/<int:teacher_id>/")
def profile(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    shedule = json.loads(teacher.shedule)
    return render_template("profile.html",
                           teacher=teacher,
                           shedule=shedule)


@blp.route('/booking/<int:id>/<string:day>/<string:hour>/')
def booking(id, day, hour):
    form = NamePhoneForm()
    return render_template("booking.html",
                           teacher=Teacher.query.get(id),
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

    teacher = Teacher.query.get(teacher_id)
    bk = Booking(student_name=name,
                 student_phone=phone,
                 teacher=teacher,
                 hour=hour,
                 day=day)
    db.session.add(bk)
    db.session.commit()

    return render_template("done.html",
                           title={"label": "Тема", "value": "Пробный урок"},
                           time={"label": days[day], "value": f"{hour}:00"},
                           name=name,
                           phone=phone)


@blp.route('/request/', methods=["GET"])
def request_view():
    form = RequestMatchingTeacherForm()
    return render_template('request.html', form=form)


@blp.route("/request_done/", methods=["POST"])
def request_done():
    goal = request.form.get('goal', 'travel')
    goal = Goal.query.filter_by(title=goal).one()
    time = request.form.get('time', '1-2')
    name = request.form['name']
    phone = request.form['phone']
    req = RequestLesson(student_name=name, student_phone=phone,
                        time_per_week=time, goal=goal)
    db.session.add(req)
    db.session.commit()

    return render_template(
        'done.html',
        title={"label": "Цель занятий", "value": req.goal.title_rus},
        time={"label": "Времени есть", "value": f"{time} часа в неделю"},
        name=req.student_name,
        phone=req.student_phone
    )


@blp.context_processor
def utility_processor():
    return dict(is_free=is_free_at_the_time)
