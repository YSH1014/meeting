from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User,load_user


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('userInfo'))

    #   return render_template('userInfo.html',user={'name':form.username.data})
    else:
        return render_template('login.html', title='Sign In', form=form)


@app.route('/userInfo')
@login_required
def userInfo():
    #用户未登录，重定向到登录界面
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return render_template('userInfo.html' )

@app.route('/logout')
def logout():
    logout_user()
    return  render_template('index.html')