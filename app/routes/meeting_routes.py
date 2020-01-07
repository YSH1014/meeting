from app import app
from app import db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting
import sqlalchemy.exc
from datetime import datetime,timedelta
from app.security import user_required


@app.route('/registerMeeting', methods=['Get', 'Post'])
@user_required
def register_meeting():
    form = RegisterMeetingForm(email=current_user.email,
                               phone=current_user.phone,
                               contact=current_user.username)
    if form.validate_on_submit():
        meeting = Meeting(
            register=current_user.id,
            status=MeetingStatusType.REGISTED,
            title=form.title.data,
            short_name=form.short_name.data,
            location=form.location.data,
            url=form.url.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            key_words=form.key_words.data,

            contact = form.contact.data,
            email=form.email.data,
            phone=form.phone.data,
            introduction=form.introduction.data
        )
        try:
            db.session.add(meeting)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for("meetingInfo", id=meeting.id))
        except sqlalchemy.exc.IntegrityError as e:
            flash('注册失败，请检查信息是否完整')

    return render_template('registerMeeting.html', form=form)


@app.route("/meetings")
def meetings():
    if current_user.is_authenticated and current_user.role == RoleType.ADMIN:  # 对管理员显示全部会议
        all_meetings = Meeting.query.all()
        return render_template('meetings.html', meetings=all_meetings)
    else:
        all_meetings = Meeting.query.filter(Meeting.status==MeetingStatusType.APPROVED)
        return render_template('meetings.html', meetings=all_meetings)


@app.route("/meetings_week")
def meetings_week():
    current_time = datetime.utcnow()
    week_after = current_time + timedelta(weeks=1)
    all_meetings = db.session.query(Meeting).filter(Meeting.status==MeetingStatusType.APPROVED).filter(current_time < Meeting.start_date ).filter(Meeting.start_date<week_after).all()
    return render_template('meetings.html', meetings=all_meetings)

@app.route("/meetingInfo/<int:id>")
def meetingInfo(id):
    meeting = Meeting.query.get(id)
    register = User.query.get(meeting.register)
    return render_template('meetingInfo.html', meeting=meeting,register=register)
