"""
run one time to load data from json file teachers.json to database test.db
"""

import json
from app.models import Teacher, Goal, db
from app import app


db.init_app(app)
app.app_context().push()


for goal, rus, favicon in (("travel", "путешествй",'⛱'),
                           ("study", "учебы", '🏫'),
                  ("work", "рабoты", '🏢'),
                 ("relocate", "переезда", '🚜')):
    gl = Goal(title=goal, title_rus=f"Для {rus}", image_location=f"{goal}.png", favicon=favicon)
    db.session.add(gl)


with open("json_data/teachers.json", "r") as f:
    teachers = json.load(f)


for t in teachers:
    teacher = Teacher(name=t["name"],
                      about=t["about"],
                      rating=t["rating"],
                      picture=t["picture"],
                      price=t["price"],
                      )

    db.session.add(teacher)
    print(f"added: {teacher}")
    goals = [Goal.query.filter_by(title=goal).one() for goal in t["goals"]]
    print(goals)
    teacher.goals = goals


db.session.commit()
print("commited")
for teacher in db.session.query(Teacher):
    print(teacher)
