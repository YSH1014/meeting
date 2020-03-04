from app import app
from app import db
from app.models import *
from datetime import date
title  = input('title')
location = input('location')
start_date = date(2020,4,1)
end_date = date(2020,4,15)

meeting = Meeting(
    register=0,
    register_time=datetime.now(),
    title=title,
    start_date=start_date,
    end_date=end_date,
    status = MeetingStatusType.APPROVED,
    lang=MeetingLanguageType.CN,
    location = location,
    location_EN="location_EN",
    email='root@xxx.xxx',
    phone='root',
    country="中国",
    country_EN="China",
    city = "北京",
    city_EN="BeiJing"
)
db.session.add(meeting)
db.session.commit()
