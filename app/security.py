from app import app
from app import db
from app.models import RoleType, User, load_user
from flask_login import current_user, login_required, login_user
from flask import render_template, current_app, request, copy_current_request_context, redirect, url_for,flash
from functools import wraps
import base64
import re
import pycurl
import io
import json
# from app.routes.user_routes import login_redirect

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


def login_redirect_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            login_redirect()
        return func(*args, **kwargs)
        


    return decorated_view

def decode_base64(data, altchars= '+/'):
    data = re.sub(r'[^a-zA-Z0-9%s]+' % altchars, '', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += '='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

def getUserInfoByCstnetId(cstnetId):
    e = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://nadc.china-vo.org/services/userinfo?callback=searcht&id='+cstnetId)
    c.setopt(c.WRITEFUNCTION, e.write)
    c.setopt(c.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
    c.perform()
    c.close()
    profile = e.getvalue().decode('UTF-8')
    print("test: "+profile)
    return profile


def createUser(profile):
    ob = json.loads(profile[8:-1])
    username = ob['truename']
    print(username)
    email = ob['cstnetId']
    print(email)
    password = ob['securityToken']
    print(password)
    address = 'no address info'
    print(address)
    phone = ob['phone']
    print(phone)

    user = User(
            username=username,
            email=email,
            # phone=phone,
            address=address,
            role=RoleType.USER
        )
    user.set_password('password')
    # print(user)
    try:
        db.session.add(user)
        db.session.commit()
        return user
        # flash('Congratulations, you are now a registered user!')
        # return redirect(url_for('login'))  # 注册成功，返回登录界面
    except Exception as err:
        print(err)
        # flash('新用户注册失败，请检查Email或手机是否已被注册')

def login_redirect(): 
    if request.cookies.get('china-vo'):
        token = request.cookies.get('china-vo')
        decodeToken = str(decode_base64(token))[2:-1]
        cstnetId, phone, token = decodeToken.split(':')
        user = User.query.filter_by(email=cstnetId).first()
        if user is None:
            try:
                profile = getUserInfoByCstnetId(cstnetId)
                user = createUser(profile)
                login_user(user)
                flash("登录成功")
                # return redirect(url_for(url))
            except:
                flash("登录失败")
                # return redirect(url_for(url))
        else:
            login_user(user)
            flash("登录成功")