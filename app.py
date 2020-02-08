from flask import Flask
import os
from flask_migrate import Migrate
from blupr_teachers import blp
from models import db


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.DebugConfig')
    app.secret_key = os.environ['SECRET_KEY']

    app.register_blueprint(blp)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)

    return app, migrate


app, migrate = create_app()

if __name__ == "__main__":
    app.run()
