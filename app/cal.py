from datetime import datetime
import caldav
from caldav.elements import dav, cdav
from app import app
from app.models import Meeting
from app import db
import traceback

client = caldav.DAVClient(url=app.config['CAL_ADMIN'])
principal = client.principal()
calendar = principal.calendar(cal_id="meeting")


def add_meeting_to_calendar(meeting):

    if meeting.start_date is None or meeting.end_date is None:
        return 
        
    id = meeting.id,
    title_CN=meeting.title if meeting.title is not None else "",
    title_EN = meeting.title_EN if meeting.title_EN is not None else "",
    theme = meeting.get_theme('zh_Hans_CN')
    if theme is not None and theme !="":
        theme = theme.replace('\r\n',r'\n')
    start_date = meeting.start_date.strftime("%Y%m%d")
    end_date = meeting.end_date.strftime("%Y%m%d")
    country = meeting.get_country('zh_Hans_CN')
    city = meeting.get_city('zh_Hans_CN')
    vcal = """
BEGIN:VCALENDAR
PRODID:-//Example Corp.//CalDAV Client//EN
VERSION:2.0
BEGIN:VEVENT
UID:{id}
SUMMARY:{title_CN}({title_EN})
DESCRIPTION:{theme}
DTSTART:{start_date}
DTEND:{end_date}
LOCATION:{country}-{city}
END:VEVENT
END:VCALENDAR
""".format(
        id = id,
        title_CN=title_CN,
        title_EN = title_EN,
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
