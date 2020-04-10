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
        id = meeting.id,
        title_CN=meeting.title if meeting.title is not None or "",
        title_EN = meeting.title_EN if meeting.title_EN is not None or "",
        theme = meeting.get_theme('zh_Hans_CN').replace('\n',r"\n"),              #需要将转义的\n替换为纯文本的\n
        start_date = meeting.start_date.strftime("%Y%m%d"),
        end_date = meeting.end_date.strftime("%Y%m%d"),
        country = meeting.get_country('zh_Hans_CN'),
        city = meeting.get_city('zh_Hans_CN')
    )

    try:
        event = calendar.add_event(vcal)
        print(event)
    except Exception as e:
        print(e)
        traceback.print_exc()
