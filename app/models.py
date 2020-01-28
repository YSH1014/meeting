from app import app, db, login
from flask_login import UserMixin
from enum import Enum, auto
from werkzeug.security import generate_password_hash, check_password_hash


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

    @staticmethod
    def from_int(x):
        if x==1:
            return MeetingLanguageType.CN
        elif x==2:
            return MeetingLanguageType.EN
        else:
            pass

    @staticmethod
    def to_int(x):
        if x==MeetingLanguageType.CN:
            return 1
        elif x==MeetingLanguageType.EN:
            return  2
        else:
            pass

    def __str__(self):
        if self == MeetingLanguageType.CN:
            return "中文"
        elif self == MeetingLanguageType.EN:
            return "English"
        else:
            return "未定义"




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,  nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    address = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), index=True, unique=True, nullable=False)
    role = db.Column(db.Enum(RoleType))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_role(self,role):
        self.role = role

    def is_admin(self):
        return self.role==RoleType.ADMIN or self.role==RoleType.ROOT

    def is_root(self):
        return self.role == RoleType.ROOT


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewer = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Enum(MeetingStatusType),nullable=False)

    title = db.Column(db.String(300),nullable=False)

    short_name = db.Column(db.String(30))
    location = db.Column(db.String(200))
    start_date = db.Column(db.Date,nullable=False)
    end_date = db.Column(db.Date,nullable=False)
    url = db.Column(db.String(200))
    key_words = db.Column(db.String(300))
    lang = db.Column(db.Enum(MeetingLanguageType))

    contact = db.Column(db.String(100))
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    introduction = db.Column(db.String(500))
