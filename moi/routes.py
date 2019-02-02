from flask import render_template, url_for, flash, redirect
from moi.models import User, Post
from moi.forms import RegistrationForm, LoginForm, LoggedForm
from moi import app, db
from flask_login import login_user, current_user, logout_user
import hashlib
import random
import string

def gen_hash(salt, text):
    joined=salt.join(text).encode('utf-8')
    for i in range(20):
        hashed=hashlib.sha256(joined).hexdigest()
        joined=hashed.encode('utf-8')
    return hashed

def gen_salt():
    salt= ''.join([random.choice(string.ascii_letters + string.digits) for n in range(20)]) 
    return salt

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        salt = gen_salt()
        hashed_password = gen_hash(salt, form.password.data)
        user = User(username=form.username.data, salt=salt, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
            
    return render_template('reg.html', title='registration', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            salt = user.salt
            password = gen_hash(salt, form.password.data)
            if password == user.password:
                login_user(user)
                return redirect(url_for('logged'))
            
    return render_template('login.html', title='registration', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('register'))

@app.route('/logged', methods=['GET','POST'])
def logged():
    form = LoggedForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        salt = user.salt
        password = gen_hash(salt, form.current_password.data)
        if password == user.password:
            user.password = gen_hash(salt, form.new_password.data)
            db.session.commit()

    return render_template('logged.html', title = 'Welcome', form=form)
