from app.models import Meeting,MeetingLanguageType
from app.forms import RegisterMeetingForm
from tools.ModelFormRender import ModelFormRender


class MeetingRender(ModelFormRender):
    def __init__(self):
        super(self.__class__,self).__init__(Meeting,RegisterMeetingForm,["location","location_EN","lang"])

    def fix_f2m(self,model,form):
        # 处理位置
        if form.location.data != None:
            location_splited = form.location.data.split('-', 2)
            if location_splited.__len__() >= 2:
                model.country = location_splited[0]
                model.city = location_splited[1]
                if location_splited.__len__()==3:
                    model.location = location_splited[2]
            else:
                model.location = form.location.data
        if form.location_EN.data != None:
            location_EN_splited = form.location_EN.data.split('-', 2)
            if location_EN_splited.__len__() >= 2:
                model.country_EN = location_EN_splited[0]
                model.city_EN = location_EN_splited[1]
                if location_splited.__len__() ==3:
                    model.location_EN = location_EN_splited[2]
            else:
                model.location_EN = form.location_EN.data

        #处理语言
        model.lang = MeetingLanguageType.from_int(form.lang.data)

    def fix_m2f(self,model,form):
        form.location.data = model.full_location()
        form.location_EN.data = model.full_location_EN()
        form.lang.data = MeetingLanguageType.to_int(model.lang)


# 预定以对象供程序直接使用
meeting_render = MeetingRender()
