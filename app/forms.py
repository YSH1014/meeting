from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField, IntegerField, \
    SelectField
from wtforms.validators import DataRequired, EqualTo, Email, URL, Regexp
from flask_login import current_user
from app.models import MeetingLanguageType


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
    # 必填项
    title = StringField('会议名称')
    title_EN = StringField('English Title')
    location = StringField('会议地点 (按照格式：国家-城市)')
    # ,description='例如：中国-北京-朝阳区大屯路甲20号国家天文台'
    location_EN = StringField('Detail location (Follow this format: Country-City)')
    # description='For example:China-Beijing-National Astronomical Observatories,20A Datun Road, Chaoyang District'

    start_date = DateField('会议开始时间 (Start Date)', validators=[DataRequired()])
    end_date = DateField('会议结束时间 (End Date)', validators=[DataRequired()])
    lang = SelectField('会议语言 (Language)', choices=[(1, '中文'), (2, 'English'), (0, '其他(Other)')], coerce=int,
                       validators=[DataRequired()])

    # 选填项
    theme = TextAreaField('会议主题')
    theme_EN = TextAreaField('Meeting Themes')
    short_name = StringField('会议简称 (Short Name)')
    url = StringField('会议网址 (Official Website)')
    key_words = StringField('关键词')
    key_words_EN = StringField('Keywords')
    # 联系方式默认自动填写
    contact = StringField('联系人姓名 (Contact)')
    email = StringField('Email')
    phone = StringField('电话 (Phone)')

    submit = SubmitField('提交 (Submit)')




class UpdateMeeting(RegisterForm):
    id = IntegerField()


class QueryMeetingById(FlaskForm):
    id = IntegerField('输入id', validators=[DataRequired()])
    submit = SubmitField('查询')


class SearchMeetingForm(FlaskForm):
    #start_date = DateField('检索开始时间')
    # end_date = DateField('检索结束时间')
    # lang = SelectField('语言', choices=[(0, '不限'), (1, '中文'), (2, 'English')], coerce=int)
    key_words = StringField('关键词')
    submit = SubmitField('检索')
