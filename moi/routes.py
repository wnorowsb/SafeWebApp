from flask import render_template, url_for, flash, redirect
from moi.models import User, Post
from moi.forms import RegistrationForm, LoginForm
from moi import app, db
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

@app.route('/login')
def login():
    form = LoginForm()
    #if form.validate_on_submit():
   #     salt = gen_salt()
  #      hashed_password = gen_hash(salt, form.password.data)
 #       user = User(username=form.username.data, salt=salt, password=hashed_password)
#        db.session.add(user)
#        db.session.commit()
#        return redirect(url_for('login'))
            
    return render_template('reg.html', title='registration', form=form)
    return "login"

