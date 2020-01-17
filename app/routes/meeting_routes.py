from app import app
from app import db
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm, UpdateMeeting
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting, MeetingLanguageType
import sqlalchemy.exc
from datetime import datetime, timedelta, date
from app.security import user_required
from sqlalchemy.sql import or_


@app.route('/registerMeeting', methods=['Get', 'Post'])
@user_required
def register_meeting():
    form = RegisterMeetingForm(email=current_user.email,
                               phone=current_user.phone,
                               contact=current_user.username)
    if form.validate_on_submit():
        meeting = Meeting(
            register=current_user.id,
            status=MeetingStatusType.REGISTERED,
            title=form.title.data,
            short_name=form.short_name.data,
            location=form.location.data,
            url=form.url.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            key_words=form.key_words.data,
            lang=MeetingLanguageType.from_int(form.lang.data),

            contact=form.contact.data,
            email=form.email.data,
            phone=form.phone.data,
            introduction=form.introduction.data
        )
        try:
            db.session.add(meeting)
            db.session.commit()
            flash('注册成功，请等待管理员审核')
            return redirect(url_for("meeting_detail", id=meeting.id))
        except sqlalchemy.exc.IntegrityError as e:
            flash('注册失败，请检查信息是否完整')

    return render_template('registerMeeting.html', form=form, action='/register_meeting')


@app.route('/update_meeting_form', methods=['get', 'post'])
@user_required
def update_meeting_form():
    id = request.args.get('id', None)
    if not id:
        return redirect(url_for('error', message='更新会议需要id作为参数'))
    meeting = Meeting.query.get(id)
    if not meeting:
        return redirect(url_for('error', message='会议不存在'))
    # 判定是否有权修改（只有已通过的会议可以进行完善）
    if meeting.status != MeetingStatusType.APPROVED:
        return redirect(url_for('error', message='会议审核中，无法修改'))
    # 去掉了权限审核页面，任何注册用户都可以修改
    '''
    if (meeting.register != current_user.id):
        return redirect(url_for('error', message='您不是该会议注册者，无法修改'))
        '''
    # 将原有属性填入新表单
    form = RegisterMeetingForm(
        title=meeting.title,
        short_name=meeting.short_name,
        location=meeting.location,
        start_date=meeting.start_date,
        end_date=meeting.end_date,
        introduction=meeting.introduction,
        url=meeting.url,
        key_words=meeting.key_words,
        contact=meeting.contact,
        email=meeting.email,
        phone=meeting.phone,
        lang=MeetingLanguageType.to_int(meeting.lang)
    )
    if form.validate_on_submit():

        meeting = Meeting.query.get(id)

        meeting.register = current_user.id
        meeting.status = MeetingStatusType.REGISTERED
        meeting.title = form.title.data
        meeting.short_name = form.short_name.data
        meeting.location = form.location.data
        meeting.url = form.url.data
        meeting.start_date = form.start_date.data
        meeting.end_date = form.end_date.data
        meeting.key_words = form.key_words.data
        meeting.contact = form.contact.data
        meeting.email = form.email.data
        meeting.phone = form.phone.data
        meeting.introduction = form.introduction.data
        meeting.lang = MeetingLanguageType.from_int(form.lang.data)
        db.session.commit()
        flash("修改成功，等待管理员再次审核")
        return redirect(url_for("meeting_detail", id=meeting.id))
    else:
        return render_template('registerMeeting.html', form=form, action=url_for('update_meeting_form', id=id))


@app.route("/meetings")
def meetings():
    try:
        query_id = request.args.get('id')
        if query_id:
            return redirect(url_for('meeting_detail', id=query_id))
        start_date = request.args.get('start_date')

        # 处理　start_date
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            start_date = date.today()

        query = Meeting.query.filter(Meeting.start_date >= start_date)
        # 处理　end_date
        end_date = request.args.get('end_date')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Meeting.start_date <= end_date)

        # 处理status
        # 如果是管理员，则读取该参数，否则用approved
        status = request.args.get('status', 'APPROVED') \
            #           if current_user.is_authenticated and current_user.role == RoleType.ADMIN else \
        #          'APPROVED'

        query = query.filter(Meeting.status == MeetingStatusType.__members__[status])

        # 处理 register
        register = request.args.get('register')
        if register:
            query = query.filter(Meeting.register == register)
        # 处理search_keywords
        search_keywords = request.args.get('keywords')
        if search_keywords:
            search_keywords = "%{}%".format(search_keywords)
            query = query.filter(or_(
                Meeting.title.like(search_keywords),
                Meeting.introduction.like(search_keywords),
                Meeting.key_words.like(search_keywords),
                Meeting.short_name.like(search_keywords)
            ))

        all_meetings = query.order_by(Meeting.start_date).all()
        return render_template('meetings.html', meetings=all_meetings)



    except ValueError as e:
        return redirect(url_for('error', message='请求参数无效，请检查日期是否存在' + e))


'''
@app.route("/meetings")
def meetings():
    start_year = request.args.get('start_year', 2020)
    start_month = request.args.get('start_month', 1)
    start_day = request.args.get('start_day', 1)
    end_year = request.args.get('end_year', 9999)
    end_month = request.args.get('end_month', 12)
    end_day = request.args.get('end_day', 31)
    status = request.args.get('status', 'all')
    try:
        start_date = date(int(start_year), int(start_month), int(start_day))
        end_date = date(int(end_year), int(end_month), int(end_day))
    except ValueError as e:
        return redirect(url_for('error', message='请求参数无效，请检查日期是否存在' + e))

    if current_user.is_authenticated \
            and current_user.role == RoleType.ADMIN \
            and status == 'registered':  # 对管理员显示未审批会议
        all_meetings = Meeting.query.filter(
            Meeting.start_date > start_date,
            Meeting.start_date < end_date,
            Meeting.status == MeetingStatusType.REGISTERED
        ).order_by(Meeting.start_date).all()
        return render_template('meetings.html', meetings=all_meetings)
    else:
        all_meetings = Meeting.query.filter(
            Meeting.status == MeetingStatusType.APPROVED,
            Meeting.start_date > start_date,
            Meeting.start_date < end_date
        ).order_by(Meeting.start_date).all()
        return render_template('meetings.html', meetings=all_meetings)
'''


@app.route("/meetings_week")
def meetings_week():
    current_time = datetime.utcnow()
    week_after = current_time + timedelta(weeks=1)
    all_meetings = db.session.query(Meeting).filter(current_time < Meeting.start_date).filter(
        Meeting.start_date < week_after).all()
    return render_template('meetings.html', meetings=all_meetings)


@app.route("/meetingInfo/<int:id>")
def meeting_detail(id):
    meeting = Meeting.query.get(id)
    if not meeting:
        return redirect(url_for('error', message='会议不存在'))
    register = User.query.get(meeting.register)
    return render_template('meeting_detail.html', meeting=meeting, register=register)


@app.route("/search_meeting")
def search_meeting():
    return render_template("search_meeting.html")
