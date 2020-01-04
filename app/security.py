from app.models import RoleType, User
from flask_login import current_user, login_required
from flask import render_template


@login_required
def admin_required(func):
    # 由于加入了login_required 装饰，进入该函数最低也是User
    if current_user.role == RoleType.USER:
        return render_template('unauthorized.html', lowest_role=RoleType.ADMIN, current_role=current_user.role)
    else:
        func()


@admin_required
def root_required(func):
    if current_user.role == RoleType.ADMIN:
        return render_template('unauthorized.html', lowest_role=RoleType.ADMIN, current_role=current_user.role)
    else:
        func()
