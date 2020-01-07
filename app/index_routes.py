from app import app
from app import db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting
import sqlalchemy.exc


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/error/<message>')
def error(message):
    return render_template('error.html',message = message)

