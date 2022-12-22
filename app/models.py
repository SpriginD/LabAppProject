from app import db
from sqlalchemy.orm import validates
from flask_login import UserMixin

from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    mail = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f'<User #{self.id}: {self.name}>'

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(16), nullable=False)
    lastname = db.Column(db.String(16), nullable=False)
    description = db.Column(db.Text(512))
    filename = db.Column(db.String(64))
    filedata = db.Column(db.LargeBinary)
    pc_no = db.Column(db.Integer, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        date = self.pub_date.strftime("%m/%d/%Y, %H:%M")
        return f'<Feedback #{self.pc_no}: {date}>'