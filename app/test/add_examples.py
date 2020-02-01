import json
from app import app
from app.models import *
from datetime import datetime,date





def postMeeting(meeting):
    meeting2 = Meeting()
    meeting2.title = meeting['title']
    meeting2.lang = 1
    meeting2.key_words = meeting['keywords']
    meeting2.location = meeting['location']
    meeting2.start_date = datetime.strptime(meeting['start'],'%Y-%m-%d')
    meeting2.end_date = datetime.strptime(meeting['end'],'%Y-%m-%d')
    meeting2.register = 1
    meeting2.status = MeetingStatusType.APPROVED

    try:
        db.session.add(meeting2)
        db.session.commit()

    except :
        print(meeting['meetingNumber'] + 'error')


fi = open('data.json','r',encoding='latin1')
meetings = json.load(fi)
i = 0
for meeting in meetings:
    postMeeting(meeting)
    print(i)
    i=i+1