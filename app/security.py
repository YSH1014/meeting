from app import app
from app.models import RoleType, User,load_user
from flask_login import current_user, login_required
from flask import render_template, current_app, request, copy_current_request_context
from functools import wraps


def push_app(func):
    def decorated_view(*args, **kwargs):
        app.app_context()
        return func(*args, **kwargs)

    return decorated_view


def user_required(func):
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return current_app.login_manager.unauthorized()

    return decorated_view


def admin_required(func):
    def decorated_view(*args, **kwargs):
        if current_user.role == RoleType.ADMIN:
            return func(*args, **kwargs)
        else:
            return current_app.login_manager.unauthorized()

    return decorated_view


def root_required(func):
    def decorated_view(*args, **kwargs):
        if current_user.role == RoleType.ROOT:
            return func(*args, **kwargs)
        else:
            return current_app.login_manager.unauthorized()

    return decorated_view
