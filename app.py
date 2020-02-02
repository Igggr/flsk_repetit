from flask import Flask
from blupr_teachers import blp
import os

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.environ.get('SECRET_KEY')
app.register_blueprint(blp)


if __name__ == "__main__":
    app.run()
