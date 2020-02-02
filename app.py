from flask import Flask
from blupr_teachers import blp
import datetime

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "secret"
app.register_blueprint(blp)


@app.template_filter()
def teachers_for_goal(teachers, goal):
    return filter(lambda teacher: goal in teacher['goals'], teachers)


@app.template_filter()
def availiable_now(teachers):
    week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    now = datetime.datetime.today()
    day = week[now.weekday()]
    hour = f"{ now.hour // 2 * 2}:00"

    def is_free(teacher):
        return teacher["free"][day][hour]

    return [teacher for teacher in teachers if is_free(teacher)]


if __name__ == "__main__":
    app.run()
