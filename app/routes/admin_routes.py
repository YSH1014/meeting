from app import app
from app import db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm, UpdateOldDataForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting, City, Country
import sqlalchemy.exc
from app.security import admin_required, login_redirect_required
from app import admin
from flask_admin.contrib.sqla import ModelView
from app.cal import add_meeting_to_calendar
# from app import bp



@app.route('/approve/<int:id>')
@admin_required
@login_redirect_required
def approve(id):
    meeting = Meeting.query.get(id)
    meeting.status = MeetingStatusType.APPROVED
    db.session.commit()
    add_meeting_to_calendar(meeting)
    return redirect(url_for('meeting_detail', id=id))


@app.route('/unapprove/<int:id>')
@admin_required
@login_redirect_required
def unapprove(id):
    meeting = Meeting.query.get(id)
    meeting.status = MeetingStatusType.UNAPPROVED
    db.session.commit()
    return redirect(url_for('meeting_detail', id=id))


@app.route('/OldDataUpdate/',methods=['get','post'])
@admin_required
def old_data_update():
    meeting = Meeting.query.filter(Meeting.cityId==None).first()
    if meeting is None :
        return redirect(url_for('index'))
    form = UpdateOldDataForm()

    if form.validate_on_submit():
        if Country.query.get(form.country.data) is None:
            country = Country(
                name_EN=form.country.data
            )
            db.session.add(country)
        if City.query.get(form.cityId.data) is None:
            city = City(
                geoId=form.cityId.data,
                name_EN=form.city.data,
                country=form.country.data
            )
            db.session.add(city)
        Meeting.query.get(form.meetingID.data).cityId = form.cityId.data
        db.session.commit()
        return redirect(url_for('old_data_update'))
    else:

        return render_template("OldDataUpdate.html",meeting=meeting,form=form)


class NadcModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


admin.add_view(NadcModelView(Meeting, db.session))
admin.add_view(NadcModelView(User, db.session))
admin.add_view(NadcModelView(Country, db.session))
admin.add_view(NadcModelView(City, db.session))
