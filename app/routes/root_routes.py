from app import app
from app import db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting
import sqlalchemy.exc
from app.security import admin_required


@app.route('/users')
#@admin_required
def users():
    allusers = User.query.all()
    return render_template('users.html', users=allusers)