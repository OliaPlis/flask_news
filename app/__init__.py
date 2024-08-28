from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'SECRET_KEY'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config.from_object('config.Config')
db = SQLAlchemy(app)

from . import models, views  # noqa

# if __name__ == '__main__':
#     app.run(debug=True)

db.create_all()

# cd C:\Users\Proffesional\PycharmProjects\pythonProject2\4\4.4\