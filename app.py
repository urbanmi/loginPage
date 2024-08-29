import os
import uuid, hashlib

from flask import Flask, render_template, request, redirect, url_for, make_response
from sqla_wrapper import SQLAlchemy

from models import User, db


app = Flask(__name__)

db_url = os.getenv("DATABASE_URL","sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)

db = SQLAlchemy(db_url)

@app.route('/')
def index():
    session_token = request.cookies.get('session_token')
    user = db.query(User).filter_by(session_token=session_token).first()
    if not user:
        return render_template('index.html')
    else:
        email = user.email
        name = user.name
        return render_template('index.html', user=user, name=name, email=email)

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('user_name')
    email = request.form.get('user_email')
    password = request.form.get('user_password')

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, password=hashed_password)
        db.add(user)
        db.commit()

    if hashed_password != user.password:
        return 'PASSWORD INCORRECT, TRY AGAIN!'

    elif hashed_password == user.password:
        session_token = str(uuid.uuid4())
        user.session_token = session_token
        user.save()
        response = make_response(redirect(url_for('index')))
        response.set_cookie('session_token', session_token, httponly=True, samesite='Strict')

    return response

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('session_token', '', -1)

    return response


if __name__ == '__main__':
    app.run(use_reloader=False, debug=False)