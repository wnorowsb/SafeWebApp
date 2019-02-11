from flask import render_template, url_for, flash, redirect,request,abort
from moi.models import User, Post
from moi.forms import RegistrationForm, LoginForm, LoggedForm, PostForm, PasswordForm
from moi import app, db
from flask_login import login_user, current_user, logout_user, login_required
import hashlib
import random
import string

def gen_hash(salt, text):
    joined=salt.join(text).encode('utf-8')
    for i in range(1000):
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
                login_user(user, remember=False)
                return redirect(url_for('home'))

    return render_template('login.html', title='registration', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('register'))

@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    # form = LoggedForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=current_user.username).first()
    #     salt = user.salt
    #     password = gen_hash(salt, form.current_password.data)
    #     if password == user.password:
    #         user.password = gen_hash(salt, form.new_password.data)
    #         db.session.commit()
    posts = Post.query.all()

    return render_template('home.html', title = 'Welcome', posts = posts)


@app.route('/change', methods=['GET','POST'])
@login_required
def changePassword():
    form = PasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        salt = user.salt
        password = gen_hash(salt, form.current_password.data)
        if password == user.password:
            user.password = gen_hash(salt, form.new_password.data)
            db.session.commit()

    return render_template('changePassword.html', title = 'ChangePassword', form=form)

@app.route('/post/new', methods=['GET','POST'])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!')
        return redirect(url_for('home'))
    return render_template('newPost.html', title='New Post', form=form, legend = "New Post")

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/edit', methods=['GET','POST'])
@login_required
def editPost(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newPost.html', title=post.title, post= post,
                           form = form,legend= "Edit Post")

@app.route('/post/<int:post_id>/delete', methods=['GET','POST'])
@login_required
def deletePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted")
    return redirect(url_for('home'))