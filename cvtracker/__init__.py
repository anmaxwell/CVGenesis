import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

#creating the db in the same directory
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

#to prevent getting stuck in circular imports create this last
from cvtracker import routes



