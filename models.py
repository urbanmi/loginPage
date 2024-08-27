import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv('DB_URL', 'sqlite:///localhost.sqlite'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=False)
    session_token = db.Column(db.String)

db.create_all()