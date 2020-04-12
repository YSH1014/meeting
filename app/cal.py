from datetime import datetime, timedelta
import caldav
from caldav.elements import dav, cdav
from app import app
from app.models import Meeting
from app import db
import traceback

url=app.config['CAL_ADMIN']
client = caldav.DAVClient(url)
principal = client.principal()
calendar = principal.calendar(cal_id="meeting")


def add_meeting_to_calendar(meeting):

    if meeting.start_date is None or meeting.end_date is None:
        return 
        
    id = meeting.id,
    title_CN=meeting.title if meeting.title else meeting.title_EN
    theme = meeting.get_theme('zh_Hans_CN')
    if theme is not None and theme !="":
        theme = theme.replace('\r\n',r'\n')
    start_date = meeting.start_date.strftime("%Y%m%d")
    end_date = (meeting.end_date + timedelta(days=1)).strftime('%Y%m%d')   # 结束日期加上1，否则日历（thunder bird为例）不显示这一天。
    country = meeting.get_country('zh_Hans_CN')
    city = meeting.get_city('zh_Hans_CN')
    vcal = """
BEGIN:VCALENDAR
PRODID:-//Example Corp.//CalDAV Client//EN
VERSION:2.0
BEGIN:VEVENT
UID:{id}
SUMMARY:{title_CN}
DESCRIPTION:{theme}
DTSTART:{start_date}
DTEND:{end_date}
LOCATION:{country}-{city}
END:VEVENT
END:VCALENDAR
""".format(
        id = id,
        title_CN=title_CN,
        theme = theme,
        start_date = start_date,
        end_date = end_date,
        country = country,
        city = city,
    )

    try:
        event = calendar.add_event(vcal)
        print(event)
    except Exception as e:
        print(e)
        traceback.print_exc()


def delete_meeting_from_calendar(id):
    try:
        event = calendar.event_by_url("{base}/({id}.ics".format(base=url,id=id))   #id前那个括号我也不知道为啥，莫名其妙。。。。
        event.delete()
        app.logger.info("%s deleteed info",id)

    except Exception as e:
        print(e)
        app.logger.warn("%d delete error",id)
        app.logger.warn(e)

    
