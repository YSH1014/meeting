from app import app
from app import db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting
import sqlalchemy.exc
from app.security import admin_required, user_required, root_required, login_redirect_required
# from app import bp

@app.route('/users')
@root_required
@login_redirect_required
def users():
    '''
    返回用户列表页
    '''
    allusers = User.query.all()
    return render_template('users.html', users=allusers)


@app.route('/set_as_admin/<int:id>')
@root_required
@login_redirect_required
def set_as_admin(id):
    '''
    将该用户设为管理员
    '''
    User.query.get(id).role = RoleType.ADMIN
    db.session.commit()
    return redirect( url_for('users'))


@app.route('/cancel_admin/<int:id>')
@root_required
@login_redirect_required
def cancel_admin(id):
    '''
    取消管理员身份
    '''
    User.query.get(id).role = RoleType.USER
    db.session.commit()
    return redirect( url_for('users'))
