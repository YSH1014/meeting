import unittest
from app import  app
from app.forms import  RegisterMeetingForm
from app.models import Meeting
from  app.ModelFormRender import  MeetingRender
from tools.ModelFormRender import  ModelFormRender

class MyTestCase(unittest.TestCase):
    def test_f2m(self):
        mfr = MeetingRender()
        meeting = Meeting()
        form = RegisterMeetingForm()
        form.title_EN.data= "aaa"
        form.location_EN.data = "a-b-c"
        mfr.f2m(meeting,form)
        assert meeting.title_EN=='aaa'
        assert meeting.country_EN=="a"
        assert  meeting.city_EN=="b"
        assert meeting.location_EN=="c"



    def test_m2f(self):
        mfr = MeetingRender()
        meeting = Meeting()
        form = RegisterMeetingForm()
        form.title_EN.data = "aaa"
        meeting.title_EN = "bbb"
        meeting.country_EN = "a"
        meeting.city_EN="b"
        meeting.location_EN="c"
        mfr.m2f(meeting, form)
        assert form.title_EN.data=="bbb"
        assert form.location_EN.data == "a-b-c"


    def setUp(self) :
        self.app_ctx = app.app_context()
        self.app_ctx.push()
        self.rq_ctx = app.test_request_context()
        self.rq_ctx.push()

    def tearDown(self) :
        self.rq_ctx.pop()
        self.app_ctx.pop()

if __name__ == '__main__':
    unittest.main()
