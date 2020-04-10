from app import app
from app.models import Meeting, MeetingStatusType
from app.cal import add_meeting_to_calendar

meetings = Meeting.query.filter(Meeting.status == MeetingStatusType.APPROVED)
for meeting in meetings:
    add_meeting_to_calendar(meeting)