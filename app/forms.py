from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField, IntegerField, \
    SelectField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Email, URL, Regexp
from flask_login import current_user
from app.models import MeetingLanguageType
from flask_babelex import _


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
    title = StringField(_('会议名称（中文）'))
    title_EN = StringField(_('会议名称（英文）'))

    #这三项不由用户显示输入，而由 cityAutoComplete回调输入
    cityId = HiddenField(validators=[DataRequired()])
    country = HiddenField(validators=[DataRequired()])
    city = HiddenField(validators=[DataRequired()])
    selector_title = HiddenField(validators=[DataRequired()])

    start_date = StringField(_('会议开始时间'))
    end_date = StringField(_('会议结束时间'))
    lang = SelectField(_('会议语言'), choices=[(1, '中文'), (2, 'English'), (0, '其他(Other)')], coerce=int,
                       validators=[DataRequired()])

    # 选填项
    theme = TextAreaField(_('会议主题（中文）'))
    theme_EN = TextAreaField(_('会议主题（英文'))
    short_name = StringField(_('会议简称'))
    url = StringField(_('会议网址'))
    key_words = StringField(_('关键词（中文）'))
    key_words_EN = StringField(_('关键词（英文）'))
    # 联系方式默认自动填写
    contact = StringField(_('联系人姓名'))
    email = StringField('Email')
    phone = StringField(_('电话'))

    submit = SubmitField(_('提交'))




class UpdateMeeting(RegisterForm):
    id = IntegerField()


class QueryMeetingById(FlaskForm):
    id = IntegerField('输入id', validators=[DataRequired()])
    submit = SubmitField('查询')


class SearchMeetingForm(FlaskForm):
    #start_date = DateField('检索开始时间')
    # end_date = DateField('检索结束时间')
    # lang = SelectField('语言', choices=[(0, '不限'), (1, '中文'), (2, 'English')], coerce=int)
    key_words = StringField(_('关键词'))
    submit = SubmitField(_('检索(Search)'))


class UpdateOldDataForm(FlaskForm):
    meetingID = IntegerField()
    cityId = HiddenField(validators=[DataRequired()])
    country = HiddenField(validators=[DataRequired()])
    city = HiddenField(validators=[DataRequired()])
    selector_title = HiddenField(validators=[DataRequired()])
    submit = SubmitField('提交')
