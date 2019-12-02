from datetime import datetime
from cvtracker import db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    role_notes = db.Column(db.String(360))
    date_opened = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mrg_id = db.Column(db.Integer, db.ForeignKey('hirer.id'), nullable=False)
    cvs = db.relationship('CV', backref="role", lazy=True)

    def __repr__(self):
        return f"Role('{self.title}', '{self.date_opened})"

class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    cv_notes = db.Column(db.String(360))
    date_entered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    mrg_id = db.Column(db.Integer, db.ForeignKey('hirer.id'), nullable=False)

    def __repr__(self):
        return f"CV('{self.surname}', '{self.date_entered})"

class Hirer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    cv = db.relationship('CV', backref="manager", lazy=True)
    role = db.relationship('Role', backref="manager", lazy=True)

    def __repr__(self):
        return f"Hirer('{self.name}')"