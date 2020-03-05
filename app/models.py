from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.exc import IntegrityError
import json
import datetime

db = SQLAlchemy()


shedule = {
    day: {i: True for i in range(8, 24, 2)}
    for day in ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
}
shedule = json.dumps(shedule)  # default shedule - always free


class SafeSavingModel:
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


class Teacher(db.Model):
    __tablename__ = "teachers"

    teacher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    picture = db.Column(db.String)
    rating = db.Column(db.Numeric)
    price = db.Column(db.Integer, nullable=False)
    about = db.Column(db.Text)
    shedule = db.Column(db.String, default=shedule, nullable=False)

    goals = db.relationship("Goal",
                            secondary="teacher_goal",
                            back_populates="teachers")
    bookings = db.relationship("Booking", back_populates="teacher")

    @hybrid_property
    def get_shedule(self):
        return json.loads(self.shedule)

    @hybrid_method
    def set_hour_state(self, day, hour, state):
        shedule = self.get_shedule
        hour = f"{hour}:00"
        shedule[day][hour] = state
        self.shedule = json.dumps(shedule)

    @hybrid_method
    def is_free_at_the_time(self, day, hour):
        return self.get_shedule[day][str(hour)]

    @hybrid_method
    def is_free_now(self):
        days = ["mon","tue","wed","thu","sun","fri","sat"]
        now = datetime.datetime.today()
        hour = now.hour // 2 * 2   # need even hour - less or equal
        day = now.weekday()
        day = days[day]
        return self.is_free_at_the_time(day, hour)

    def __repr__(self):
        return f"Teacher<id: {self.teacher_id}, name: {self.name}, " \
               f"rating: {self.rating}, price:{self.price}>"


teacher_goal = db.Table("teacher_goal",
                        db.Column("teacher_id", db.Integer,
                                  db.ForeignKey("teachers.teacher_id"),
                                  primary_key=True, nullable=False),
                        db.Column("goal_id", db.Integer,
                                  db.ForeignKey("goals.goal_id"),
                                  primary_key=True, nullable=False)
                        )


class Goal(db.Model):
    __tablename__ = "goals"

    goal_id = db.Column("goal_id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(15))
    title_rus = db.Column('title_rus', db.String(15))
    favicon = db.Column('favicon', db.String(1))
    image_location = db.Column("image_location", db.String(30))

    teachers = db.relationship("Teacher",
                               secondary="teacher_goal",
                               back_populates="goals")
    lesson_requests = db.relationship("RequestLesson", back_populates="goal")

    def __repr__(self):
        return f"Goal<id : {self.goal_id}, title: {self.title}>"


class RequestLesson(db.Model, SafeSavingModel):
    __tablename__ = "request_lessons"

    request_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String, nullable=False)
    student_phone = db.Column(db.String, nullable=False)
    time_per_week = db.Column(db.Integer, nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.goal_id"),
                        nullable=False)

    goal = db.relationship("Goal", back_populates="lesson_requests")

    def __repr__(self):
        return f"RequestLesson<name: {self.student_name}," \
               f"phone: {self.student_phone}, " \
               f"time: {self.time_per_week}, "  \
               f"goal: {self.goal.title} >"


class Booking(db.Model, SafeSavingModel):
    __tablename__ = "bookings"

    booking_id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.teacher_id"),
                           nullable=False)
    day = db.Column(db.String, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    student_name = db.Column(db.String, nullable=False)
    student_phone = db.Column(db.String, nullable=False)

    teacher = db.relationship("Teacher", back_populates="bookings")

    def __repr__(self):
        return f"Booking<name: {self.student_name}," \
               f"phone: {self.student_phone}," \
               f"teacher: {self.teacher}," \
               f"day: {self.day}," \
               f"hour: {self.hour}"
