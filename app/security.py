from app.models import RoleType, User
from flask_login import current_user, login_required
from flask import render_template,current_app,request,copy_current_request_context
from functools import wraps


@login_required
def admin_required(func):
    # 由于加入了login_required 装饰，进入该函数最低也是User
    @wraps(func)
    @copy_current_request_context
    def decorated_view(*args, **kwargs):
        return func(*args, **kwargs)
    return decorated_view()

'''
@admin_required
def root_required(func):
    @copy_current_request_context
    def decorated_view(*args, **kwargs):
        return func(*args, **kwargs)

    return decorated_view()
'''