from flask import render_template, Blueprint
from forms import NamePhoneForm, RequestMatchingTeacherForm
from models import Teacher, Goal, RequestLesson, Booking

blp = Blueprint('blp', __name__)

days = {"mon": "Понедельник",
        "tue": "Вторник",
        "wed": "Среда",
        "thu": "Четверг",
        "sun": "Воскресенье",
        "fri": "Пятница",
        "sat": "Суббота",
        }


@blp.route("/")
def index():
    """покажет не более 6 самых высокорейтинговых
    из доступных сейчас учителей """
    teachers = Teacher.query.order_by(Teacher.rating.desc()).limit(6)

    return render_template("index.html",
                           teachers=teachers,
                           goals=Goal.query,
                           only_free_now=True)


@blp.route("/all/")
def index_all():
    """покажет 6 самых высокорейтиноговых учителей"""
    teachers = Teacher.query.order_by(Teacher.rating.desc()).limit(6)
    return render_template("index.html",
                           teachers=teachers,
                           goals=Goal.query)


@blp.route("/goals/<goal>/")
def goal_view(goal):
    goal = Goal.query.filter_by(title=goal).one()
    return render_template("goal.html", goal=goal,
                           teachers=goal.teachers)


@blp.route("/profiles/<int:teacher_id>/")
def profile(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    return render_template("profile.html",
                           teacher=teacher)


@blp.route('/booking/<int:teacher_id>/<string:day>/<string:hour>/',
           methods=["GET", "POST"])
def booking(teacher_id, day, hour):
    form = NamePhoneForm()
    if form.validate_on_submit():
        bk = Booking(teacher_id=teacher_id, day=day, hour=hour)
        form.populate_obj(bk)  # student_name and student_phone
        teacher = Teacher.query.get(teacher_id)
        teacher.set_hour_state(day, hour, False)  # теперь время - занято
        bk.save()
        return render_template(
             "done.html",
             title={"label": "Тема", "value": "Пробный урок"},
             time={"label": days[bk.day],
                   "value": f"{bk.hour}:00"},
             name=bk.student_name,
             phone=bk.student_phone
        )

    return render_template("booking.html",
                           teacher=Teacher.query.get(teacher_id),
                           time={"day": day, "hour": hour},
                           days=days,
                           form=form
                           )


@blp.route('/request/', methods=["GET", "POST"])
def request_view():
    form = RequestMatchingTeacherForm()
    req_lesson = RequestLesson()
    if form.validate_on_submit():
        form.populate_obj(req_lesson)
        req_lesson.save()
        return render_template(
            'done.html',
            title={"label": "Цель занятий",
                   "value": req_lesson.goal.title_rus},
            time={"label": "Времени есть",
                  "value": f"{req_lesson.time_per_week} часа в неделю"},
            name=req_lesson.student_name,
            phone=req_lesson.student_phone
        )
    return render_template('request.html', form=form)
