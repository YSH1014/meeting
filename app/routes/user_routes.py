from app import app
from app import db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting
from app.security import user_required
import sqlalchemy.exc
# from app import bp

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


@app.route('/userInfo')
@user_required
def userInfo():
    # 用户未登录，重定向到登录界面
    if not current_user.is_authenticated:
        flash("请登录")
        return redirect(url_for('index'))

    return render_template('userInfo.html')


@app.route('/logout')
@user_required
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/register', methods=['Get', 'Post'])
def register():
    if current_user.is_authenticated:
        flash('您已登录')
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            role=RoleType.USER
        )
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))  # 注册成功，返回登录界面
        except sqlalchemy.exc.IntegrityError as e:
            flash('注册失败，请检查Email或手机是否已被注册')
    # 输入无效或添加用户发生异常（Email重复等原因），返回注册界面
    return render_template('register.html', title='Register', form=form)

