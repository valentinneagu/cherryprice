from __init__ import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"


class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.token}')"
