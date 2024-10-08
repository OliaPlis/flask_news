from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Необходимо авторизоваться!'
login_manager.login_message_category = 'alert-warning'

from . import models, views  # noqa

db.create_all()
# cd C:\Users\Proffesional\PycharmProjects\pythonProject2\4\flask_news\
# flask run --debug
