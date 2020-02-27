from app import app
from app import db
from flask import render_template, redirect, url_for, flash, request, current_app, jsonify, make_response
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting
import sqlalchemy.exc
# from app.routes.user_routes import login_redirect
from app.security import login_redirect_required
from flask_babelex import Babel, _

from app import babel

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

@app.route('/set-locale/<locale>')
def set_locale(locale):
    if locale not in current_app.config['LANGUAGES']:
        locale = current_app.config['LANGUAGES'][0]

    response = make_response(jsonify(message=_('Setting updated.')))
    if current_user.is_authenticated:
        current_user.locale = locale
        db.session.commit()
    else:
        response.set_cookie('locale', locale, max_age=60 * 60 * 24 * 30)
    return response

# @app.before_app_request
# def before_request():
#     g.locale = str(get_locale())

@babel.localeselector
def get_locale():
    if current_user.is_authenticated and current_user.locale is not None:
        if current_user.locale in current_app.config['LANGUAGES']:
            return current_user.locale

    locale = request.cookies.get('locale')
    if locale is not None:
        if locale in current_app.config['LANGUAGES']:
            return locale
    locale = request.accept_languages.best_match(current_app.config['LANGUAGES'])
    if locale is None:
        if len(current_app.config['LANGUAGES']) > 0:
            locale = current_app.config['LANGUAGES'][0]
    if locale is None:
        locale = 'zh_Hans_CN'
    if locale not in current_app.config['LANGUAGES']:
        locale = 'en'
    return locale