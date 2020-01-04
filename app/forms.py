from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('姓名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重新输入密码', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('电话号码+86', validators=[DataRequired()])
    address = StringField('地址')
    submit = SubmitField('注册')


class RegisterMeetingForm(FlaskForm):
    title = StringField('会议题目', validators=[DataRequired()])
    short_name = StringField('会议简称')
    location = StringField('会议地点', validators=[DataRequired()])
    start_date = DateTimeField('会议开始时间 格式形如："2020-1-1 12:00:00"', validators=[DataRequired()])
    end_date = DateTimeField('会议结束时间', validators=[DataRequired()])
    introduction = TextAreaField('会议简介')
    url = StringField('会议链接')

    # 默认自动填写
    name = StringField('联系人姓名', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('电话+ 86', validators=[DataRequired()])

    submit = SubmitField('提交')