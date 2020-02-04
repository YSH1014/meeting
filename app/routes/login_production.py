from flask import request, redirect, make_response, flash, url_for
from flask_login import login_user
from app import app
from app.models import User
from app.security import decode_base64, getUserInfoByCstnetId, createUser


@app.route('/login',methods = ['GET', 'POST'])
def login():
    if not request.cookies.get('china-vo'):
        referrer = request.headers.get("Referer")
        redirect_to_login  = redirect("http://passport.china-vo.org/loginFrm?umt=true")
        response = make_response(redirect_to_login)
        print(referrer)
        if referrer is None:
            response.set_cookie('cvoumt', "\"https://nadc.china-vo.org/meetings/login\"", max_age=3600 * 24, path = '/', domain='china-vo.org')
        else:
            response.set_cookie('cvoumt', "\""+referrer+"\"", max_age=3600 * 24, path = '/', domain='china-vo.org')

        # response.set_cookie('cvoumt', "", max_age=3600 * 24, path = '/', domain='china-vo.org')
        return redirect_to_login

    else:
        token = request.cookies.get('china-vo')
        decodeToken = str(decode_base64(token))[2:-1]
        cstnetId, phone, token = decodeToken.split(':')
        user = User.query.filter_by(email=cstnetId).first()
        if user is None:
            try:
                # print("get user info by cstnetId")
                profile = getUserInfoByCstnetId(cstnetId)
                # print(profile)
                user = createUser(profile)
                login_user(user)
                flash("登录成功")
                return redirect(url_for('userInfo'))
            except:
                flash("登录失败")
                return redirect(url_for('index'))
        else:
            login_user(user)
            flash("登录成功")
            return redirect(url_for('userInfo'))
