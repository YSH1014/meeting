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
SUMMARY:{theme}
DTSTART:{start_date}
DTEND:{end_date}
LOCATION:{country}-{city}
END:VEVENT
END:VCALENDAR
""".format(
        id = meeting.id,
        theme = meeting.get_theme('zh_Hans_CN'),
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
