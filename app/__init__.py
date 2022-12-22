from flask import Flask, url_for

from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin

from flask_login import LoginManager, current_user, login_user, logout_user

app = Flask(__name__)

if app.config["DEBUG"] == True:
    app.config.from_object('settings.DevelopmentConfig')
else:
    app.config.from_object('settings.ProductionConfig')

db = SQLAlchemy(app)
login = LoginManager(app)

from app.models import Feedback
from app import views

admin = Admin(app, index_view=views.MyAdminView())
admin.add_view(views.MyModelView(Feedback, db.session))

login.login_view = 'login'