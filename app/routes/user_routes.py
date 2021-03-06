from app import app
from app import db
from flask import render_template, redirect, url_for, flash, session,request,make_response
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting
from app.routes.meeting_routes import query_meetings
from app.security import user_required
import sqlalchemy.exc
import base64
import re
if app.config["ENV"]=="production":
    import pycurl
import io
import json
from app.security import decode_base64, createUser, getUserInfoByCstnetId, login_redirect_required,logout_passport



# def decode_base64(data, altchars= '+/'):
#     data = re.sub(r'[^a-zA-Z0-9%s]+' % altchars, '', data)  # normalize
#     missing_padding = len(data) % 4
#     if missing_padding:
#         data += '='* (4 - missing_padding)
#     return base64.b64decode(data, altchars)

# def getUserInfoByCstnetId(cstnetId):
#     e = io.BytesIO()
#     c = pycurl.Curl()
#     c.setopt(c.URL, 'http://astrocloud.china-vo.org/services/userinfo?callback=searcht&id='+cstnetId)
#     c.setopt(c.WRITEFUNCTION, e.write)
#     c.setopt(c.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
#     c.perform()
#     c.close()
#     profile = e.getvalue().decode('UTF-8')
#     print(profile)
#     return profile


# def createUser(profile):
#     ob = json.loads(profile[8:-1])
#     username = ob['truename']
#     print(username)
#     email = ob['cstnetId']
#     print(email)
#     password = ob['securityToken']
#     print(password)
#     address = 'no address info'
#     print(address)
#     phone = ob['phone']
#     print(phone)

#     user = User(
#             username=username,
#             email=email,
#             phone=phone,
#             address=address,
#             role=RoleType.USER
#         )
#     user.set_password(password)
#     print(user)
#     try:
#         db.session.add(user)
#         db.session.commit()
#         return user
#         # flash('Congratulations, you are now a registered user!')
#         # return redirect(url_for('login'))  # 注册成功，返回登录界面
#     except sqlalchemy.exc.IntegrityError as e:
#         print(e)
#     #     flash('新用户注册失败，请检查Email或手机是否已被注册')

# def login_redirect(): 
#     if request.cookies.get('china-vo'):
#         token = request.cookies.get('china-vo')
#         decodeToken = str(decode_base64(token))[2:-1]
#         cstnetId, phone, token = decodeToken.split(':')
#         user = User.query.filter_by(email=cstnetId).first()
#         if user is None:
#             try:
#                 profile = getUserInfoByCstnetId(cstnetId)
#                 user = createUser(profile)
#                 login_user(user)
#                 flash("登录成功")
#                 # return redirect(url_for(url))
#             except:
#                 flash("登录失败")
#                 # return redirect(url_for(url))
#         else:
#             login_user(user)
#             flash("登录成功")

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))

#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         # 返回错误信息
#         if user is None:
#             flash("用户不存在")
#             return redirect(url_for('login'))
#         elif not user.check_password(form.password.data):
#             flash('密码错误')
#             return redirect(url_for('login'))

#         #登录成功
#         login_user(user, remember=form.remember_me.data)
#         flash("登录成功")
#         return redirect(url_for('userInfo'))

#     #   return render_template('userInfo.html',user={'name':form.username.data})
#     else:
#         return render_template('login.html', title='Sign In', form=form)


@app.route('/userInfo')
@user_required
@login_redirect_required
def userInfo():
    # 用户未登录，重定向到登录界面
    if not current_user.is_authenticated:
        flash("请登录")
        return redirect(url_for('index'))

    meetings = query_meetings(register=current_user.id)
    return render_template('userInfo.html',meetings=meetings)


@app.route('/logout')
@user_required
def logout():
    logout_user()
    logout_passport()
    redirect_to_index  = redirect(url_for('index'))
    response = make_response(redirect_to_index)
    response.set_cookie('china-vo','', expires=0, path='/',domain="china-vo.org")  
    return redirect_to_index



# @app.route('/logout_new')
# @user_required
# def logout_new():
#     logout_user()

#     return render_template('index.html')


@app.route('/register', methods=['Get', 'Post'])
def register():
    if current_user.is_authenticated:
        flash('您已登录')
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            role=RoleType.USER
        )
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))  # 注册成功，返回登录界面
        except sqlalchemy.exc.IntegrityError as e:
            flash('注册失败，请检查Email或手机是否已被注册')
    # 输入无效或添加用户发生异常（Email重复等原因），返回注册界面
    return render_template('register.html', title='Register', form=form)

