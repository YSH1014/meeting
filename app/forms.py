from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('姓名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重新输入密码', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('电话', validators=[DataRequired()])
    address = StringField('地址')
    submit = SubmitField('注册')


class RegisterMeetingForm(FlaskForm):
    title = StringField('会议题目', validators=[DataRequired()])
    short_name = StringField('会议简称')
    location = StringField('会议地点', validators=[DataRequired()])
    start_date = DateField('会议开始时间', validators=[DataRequired()])
    end_date = DateField('会议结束时间', validators=[DataRequired()])
    introduction = TextAreaField('会议简介')
    url = StringField('会议链接')
    key_words=StringField('关键词')
    # 默认自动填写
    contact = StringField('联系人姓名', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('电话', validators=[DataRequired()])

    submit = SubmitField('提交')