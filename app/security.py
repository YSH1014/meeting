from app import app
from app.models import RoleType, User, load_user
from flask_login import current_user, login_required
from flask import render_template, current_app, request, copy_current_request_context, redirect, url_for,flash
from functools import wraps


@app.route('/unauthorized/<role_require>')
def unauthorized(role_require):
    return render_template('unauthorized.html', role_required=role_require,
                           current_role=current_user.role if current_user.is_authenticated else 'tourist')


def user_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            flash("您需要登陆后执行该操作")
            return redirect(url_for('login', role_require=RoleType.USER))

    return decorated_view


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin():
            return func(*args, **kwargs)
        else:
            return redirect(url_for('unauthorized', role_require=RoleType.ADMIN))

    return decorated_view


def root_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_root():
            return func(*args, **kwargs)
        else:
            return redirect(url_for('unauthorized', role_require=RoleType.ROOT))

    return decorated_view
