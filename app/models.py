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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewer = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Enum(MeetingStatusType),nullable=False)
    title = db.Column(db.String(100),nullable=False)
    short_name = db.Column(db.String(30))
    location = db.Column(db.String(200))
    start_date = db.Column(db.Date,nullable=False)
    end_date = db.Column(db.Date,nullable=False)
    url = db.Column(db.String(200))
    key_words = db.Column(db.String(100))

    contact = db.Column(db.String(30))
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    introduction = db.Column(db.String(500))
