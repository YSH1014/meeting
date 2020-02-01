from app import app
from app import db
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting
import sqlalchemy.exc
# from app.routes.user_routes import login_redirect
from app.security import login_redirect_required
# from app import bp

@app.route('/')
@app.route('/index')
@login_redirect_required
def index():
    # if not current_user.is_authenticated:
        # print('test')
        # login_redirect()
    return render_template('index.html')
    # else:
    #     # print('test1')
    #     return render_template('index.html')
        
    


@app.route('/error/<message>')
def error(message):
    return render_template('error.html',message = message)

