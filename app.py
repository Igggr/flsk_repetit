from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "main"


@app.route("/goals/<goal>")
def goal_v(goal):
    return f"goal {goal}"


@app.route("/profiles/<int:id>")
def profile(teacher_id):
    return f"iteacher id {teacher_id}"


if __name__ == "__main__":
    app.run()
