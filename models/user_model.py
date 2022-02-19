from sqlalchemy.orm import relationship

from db import db


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(), unique=True)
    name = db.Column(db.String())
    password = db.Column(db.String())
    bills = relationship("Bill", backref='parent', cascade="all, delete-orphan")
