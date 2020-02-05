from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField,IntegerField,SelectField
from wtforms.validators import DataRequired, EqualTo, Email
from flask_login import current_user
from  app.models import MeetingLanguageType

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
    title = StringField('会议名称', validators=[DataRequired()])
    short_name = StringField('会议简称')
    country = StringField('会议所在国家',validators=[DataRequired()])
    city = StringField('会议所在城市',validators=[DataRequired()])
    location = StringField('会议详细地点', validators=[DataRequired()])
    start_date = DateField('会议开始时间', validators=[DataRequired()])
    end_date = DateField('会议结束时间', validators=[DataRequired()])
    introduction = TextAreaField('会议主题',validators=[DataRequired()])
    introduction_EN = TextAreaField('会议主题（英文）')

    url = StringField('会议网址')
    key_words=StringField('关键词')
    lang = SelectField('会议语言',choices=[(1,'中文'),(2,'英文'),(0,'其他')],coerce=int)
    # 联系方式默认自动填写
    contact = StringField('联系人姓名', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('电话', validators=[DataRequired()])

    submit = SubmitField('提交')


class UpdateMeeting(RegisterForm):
    id = IntegerField()


class QueryMeetingById(FlaskForm):
    id = IntegerField('输入id',validators=[DataRequired()])
    submit = SubmitField('查询')


class SearchMeetingForm(FlaskForm):
    start_date = DateField('检索开始时间')
    end_date = DateField('检索结束时间')
    lang = SelectField('语言',choices=[(0,'不限'),(1,'中文'),(2,'英文')],coerce=int)
    key_words=StringField('关键词')
    submit = SubmitField('搜索')
