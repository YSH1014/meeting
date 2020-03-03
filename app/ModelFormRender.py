from app.models import Meeting, MeetingLanguageType, City, Country
from app.forms import RegisterMeetingForm
from tools.ModelFormRender import ModelFormRender
from app import db


class MeetingRender(ModelFormRender):
    def __init__(self):
        super(self.__class__, self).__init__(Meeting, RegisterMeetingForm,
                                             ["location", "location_EN", "lang", 'city', 'country','selector_title'])

    def fix_f2m(self, model, form):

        if Country.query.get(form.country.data) is None:
            country = Country(name_EN=form.country.data)
            db.session.add(country)
        if City.query.get(form.cityId.data) is None:
            city = City(geoId=form.cityId.data,
                        name_EN=form.city.data,
                        country=form.country.data,
                        selector_title=form.selector_title.data)
            db.session.add(city)

        db.session.commit()

        # 处理语言
        model.lang = MeetingLanguageType.from_int(form.lang.data)

    def fix_m2f(self, model, form):
        city = City.query.get(model.cityId)
        if city is not None:
            form.city.data = city.name_EN
            form.country.data = city.country
            form.cityId.data = model.cityId
            form.selector_title.data = city.selector_title
        form.lang.data = MeetingLanguageType.to_int(model.lang)


# 预定以对象供程序直接使用
meeting_render = MeetingRender()
