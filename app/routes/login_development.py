from flask import render_template, redirect, flash, url_for
from flask_login import login_user, current_user
from app import app
from app.forms import LoginForm
from app.models import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # 返回错误信息
        if user is None:
            flash("用户不存在")
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            flash('密码错误')
            return redirect(url_for('login'))

        #登录成功
        login_user(user, remember=form.remember_me.data)
        flash("登录成功")
        return redirect(url_for('userInfo'))

    #   return render_template('userInfo.html',user={'name':form.username.data})
    else:
        return render_template('login.html', title='Sign In', form=form)