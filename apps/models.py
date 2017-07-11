from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash as genpass


db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, nullable=False, autoincrement=True,
                    primary_key=True)
    username = db.Column(db.String(12), unique=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(), unique=True)
    is_admin = db.Column(db.Boolean())

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = genpass(password)
        self.is_admin = False


    def __repr__(self):
        return "{}".format(self.username)
