from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.models import db, Teacher, Goal, Booking, RequestLesson
admin = Admin()

admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Goal, db.session))
admin.add_view(ModelView(Booking, db.session))
admin.add_view(ModelView(RequestLesson, db.session))

