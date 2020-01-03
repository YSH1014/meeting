from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisteForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email])
    phone = StringField('Phone Number + 86', validators=[DataRequired()])
    submit = SubmitField('注册')


class RegisteMeetingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])
    start_date = DateTimeField('Start DateTime', validators=[DataRequired()])
    end_date = DateTimeField('End Date Time', validators=[DataRequired()])
    introduction = TextAreaField('Introduction')

    # 联系方式，若勾选“使用我的联系方式”则自动填写
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email])
    phone = StringField('Phone Number + 86', validators=[DataRequired()])
