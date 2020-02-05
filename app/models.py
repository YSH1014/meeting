from app import app, db, login
from flask_login import UserMixin
from enum import Enum, auto
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class RoleType(Enum):
    USER = auto()
    ADMIN = auto()
    ROOT = auto()


class MeetingStatusType(Enum):
    REGISTERED = auto()  # 已注册，待审核
    APPROVED = auto()  # 审核通过
    UNAPPROVED = auto()  # 审核未通过
    OUTDUE = auto()  # 过期


class MeetingLanguageType(Enum):
    CN = auto()
    EN = auto()
    OTHER = auto()
    @staticmethod
    def from_int(x):
        if x == 1:
            return MeetingLanguageType.CN
        elif x == 2:
            return MeetingLanguageType.EN
        else:
            pass

    @staticmethod
    def to_int(x):
        if x == MeetingLanguageType.CN:
            return 1
        elif x == MeetingLanguageType.EN:
            return 2
        else:
            return 0

    def __str__(self):
        if self == MeetingLanguageType.CN:
            return "中文"
        elif self == MeetingLanguageType.EN:
            return "English"
        else:
            return "其他"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    address = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), index=True)
    role = db.Column(db.Enum(RoleType))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_role(self, role):
        self.role = role

    def is_admin(self):
        return self.role == RoleType.ADMIN or self.role == RoleType.ROOT

    def is_root(self):
        return self.role == RoleType.ROOT


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewer = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Enum(MeetingStatusType), nullable=False)
    register_time = db.Column(db.DateTime, default=datetime(2020, 1, 1, 0, 0, 0))

    title = db.Column(db.String(300), nullable=False)

    short_name = db.Column(db.String(30))
    country = db.Column(db.String(50))
    city = db.Column(db.String(30))
    location = db.Column(db.String(200))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    url = db.Column(db.String(200))
    key_words = db.Column(db.Text())
    lang = db.Column(db.Enum(MeetingLanguageType))

    contact = db.Column(db.String(100))
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(60), nullable=False)
    introduction = db.Column(db.Text())
    introduction_EN=db.Column(db.Text())

    def update_from_form(self, form):
        from app.forms import RegisterMeetingForm
        if isinstance(form, RegisterMeetingForm):
            self.title = form.title.data
            self.short_name = form.short_name.data
            self.country = form.country.data
            self.city = form.city.data
            self.location = form.location.data
            self.start_date = form.start_date.data
            self.end_date = form.end_date.data
            self.url = form.end_date.data
            self.key_words = form.key_words.data
            self.lang = MeetingLanguageType.from_int(form.lang.data)
            self.contact = form.contact.data
            self.email = form.email.data
            self.phone = form.phone.data
            self.introduction = form.introduction.data
            self.introduction_EN  = form.introduction_EN.data
        else:
            raise Exception("传入form应为RegisterMeetingForm类型")

    def full_location(self):
        return "{country},{city},{location}".format(
            country=self.country,
            city=self.city,
            location=self.location
        )
