from datetime import datetime
from cvtracker import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    role_notes = db.Column(db.String(360))
    date_opened = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mgr_id = db.Column(db.Integer, db.ForeignKey('hirer.id'), nullable=False)
    rolestatus_id = db.Column(db.Integer, db.ForeignKey('rolestatus.id'), nullable=False)
    cvs = db.relationship('CV', backref="role", lazy=True)

    def __repr__(self):
        return f"Role('{self.title}', '{self.date_opened})"

class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(60), nullable=False)
    cv_notes = db.Column(db.String(360))
    date_entered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=False)
    cvstatus_id = db.Column(db.Integer, db.ForeignKey('cvstatus.id'), nullable=False)
    cvchange = db.relationship('Statuschange', backref="cvchange", lazy=True)

    def __repr__(self):
        return f"CV('{self.reference}', '{self.date_entered})"

class Hirer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    role = db.relationship('Role', backref="mgrrole", lazy=True)

    def __repr__(self):
        return f"Hirer(#{self.id}, '{self.name}')"

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    cv = db.relationship('CV', backref="cvsource", lazy=True)

    def __repr__(self):
        return f"Source(#{self.id}, '{self.name}')"

class Cvstatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    cvstatus = db.relationship('CV', backref="cvstatus", lazy=True)
    statuschange = db.relationship('Statuschange', backref="statuschange", lazy=True)

    def __repr__(self):
        return f"CVStatus(#{self.id}, '{self.name}')"

class Rolestatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    rolestatus = db.relationship('Role', backref="rolestatus", lazy=True)

    def __repr__(self):
        return f"RoleStatus(#{self.id}, '{self.name}')"

class Statuschange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_changed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status_id = db.Column(db.Integer, db.ForeignKey('cvstatus.id'), nullable=False)
    cv_id = db.Column(db.Integer, db.ForeignKey('CV.id'), nullable=False)

    def __repr__(self):
        return f"Status Changes"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.email}')"