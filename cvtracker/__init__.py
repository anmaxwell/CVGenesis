import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
#adding security for login
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#creating the db in the same directory
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

#to prevent getting stuck in circular imports create this last
from cvtracker import routes, models



