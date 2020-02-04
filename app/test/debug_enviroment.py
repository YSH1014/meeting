from flask import url_for, flash, render_template
from werkzeug.utils import redirect

from app import  app
from app import security
from app import db
from flask_login import current_user,login_user

from app.forms import LoginForm
from app.models import *


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # 返回错误信息
        if user is None:
            flash("用户不存在")
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            flash('密码错误')
            return redirect(url_for('login'))

        #登录成功
        login_user(user, remember=form.remember_me.data)
        flash("登录成功")
        return redirect(url_for('userInfo'))

     #   return render_template('userInfo.html',user={'name':form.username.data})
    else:
        return render_template('login.html', title='Sign In', form=form)

def generate_user():
    root = User(
        username="root",
        email="root@xxx.xxx",
        address="root"
                )
    db.session.add(root)
    root.set_password('root')
    root.set_role(RoleType.ROOT)
    db.session.commit()
    return root

#建立初始数据
db.drop_all()
db.create_all()
user = generate_user()
#创建app_ctx
app_ctx = app.app_context()
app_ctx.push()

request_ctx = app.test_request_context()
request_ctx.push()
login_user(user)
request_ctx.pop()

app_ctx.pop()
db.drop_all()



