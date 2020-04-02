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
    def from_int(x: int) :
        '''
            从整形变量得到MeetingLanguageType
        '''
        if x == 0:
            return MeetingLanguageType.OTHER
        if x == 1:
            return MeetingLanguageType.CN
        elif x == 2:
            return MeetingLanguageType.EN
        else:
            pass

    @staticmethod
    def to_int(x) -> int:
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
    locale = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_role(self, role: RoleType):
        '''
            设置用户的role
        '''
        self.role = role

    def is_admin(self):
        return self.role == RoleType.ADMIN or self.role == RoleType.ROOT

    def is_root(self):
        return self.role == RoleType.ROOT


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Meeting(db.Model):
    # 由程序填写的信息
    id = db.Column(db.Integer, primary_key=True)
    register = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewer = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Enum(MeetingStatusType), nullable=False)
    register_time = db.Column(
        db.DateTime, default=datetime(2020, 1, 1, 0, 0, 0))

    # 用户必填信息
    title = db.Column(db.String(300))
    title_EN = db.Column(db.String(300))
    # 从Country到location_EN，数据更新完后不再使用
    country = db.Column(db.String(50))
    country_EN = db.Column(db.String(50))
    city = db.Column(db.String(50))
    city_EN = db.Column(db.String(50))
    location = db.Column(db.String(200))
    location_EN = db.Column(db.String(200))
    # ------------
    cityId = db.Column(db.Integer, db.ForeignKey("city.geoId"))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    lang = db.Column(db.Enum(MeetingLanguageType))

    # 选填信息
    url = db.Column(db.String(200))
    key_words = db.Column(db.Text())
    key_words_EN = db.Column(db.Text())
    short_name = db.Column(db.String(30))
    contact = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(60))
    theme = db.Column(db.Text())
    theme_EN = db.Column(db.Text())

    def full_location(self):
        '''
            已弃用
        '''
        if self.country and self.city:
            return "{country}-{city}".format(
                country=self.country,
                city=self.city,
            )
        else:
            return self.location

    def full_location_EN(self):
        '''
            已弃用
        '''
        if self.country_EN and self.city_EN:
            return "{country}-{city}".format(
                country=self.country_EN,
                city=self.city_EN,
            )
        else:
            return self.location_EN

    def get_country(self, locale: str):
        '''
        根据locale得到相应语言的国家（当前只支持中-英），若没有中文，返回英文
        '''
        country = Country.query.get(
            City.query.get(self.cityId).country
        )
        if locale == "en":
            return country.name_EN
        else:
            return country.name_CN if country.name_CN is not None else country.name_EN

    def get_city(self, locale):
        '''
        根据locale得到相应语言的城市（当前只支持中-英），若没有中文，返回英文
        '''
        city = City.query.get(self.cityId)
        if locale == "en":
            return city.name_EN
        else:
            return city.name_CN if city.name_CN is not None else city.name_EN

    def get_location(self, locale):
        location = self.get_country(locale) + ' - ' + self.get_city(locale)
        return location

    def get_theme(self, locale):
        if locale == "en":
            return self.theme_EN if self.theme_EN is not None else self.theme
        else:
            return self.theme if self.theme is not None else self.theme_EN

    def get_keyWords(self, locale):
        if locale == "en":
            return self.key_words_EN if self.key_words_EN is not None else self.key_words
        else:
            return self.key_words if self.key_words is not None else self.key_words_EN
    
    


class Country(db.Model):
    name_EN = db.Column(db.String(50), primary_key=True)
    name_CN = db.Column(db.String(50))


class City(db.Model):
    geoId = db.Column(db.Integer, primary_key=True)
    name_EN = db.Column(db.String(50))
    name_CN = db.Column(db.String(50))
    country = db.Column(db.String(50), db.ForeignKey('country.name_EN'))
    selector_title = db.Column(db.String(200))
