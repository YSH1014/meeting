from app import app
from app import db
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm, UpdateMeeting, SearchMeetingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting, MeetingLanguageType
import sqlalchemy.exc
from datetime import datetime, timedelta, date
from app.security import user_required, login_redirect_required
from sqlalchemy.sql import or_,desc
from app.ModelFormRender import meeting_render
from flask_babelex import _
from app.index_routes import get_locale


@app.route('/registerMeeting', methods=['Get', 'Post'])
@user_required
@login_redirect_required
def register_meeting():
    form = RegisterMeetingForm(email=current_user.email,
                               phone=current_user.phone,
                               contact=current_user.username)
    if form.validate_on_submit():
        meeting = Meeting()
        # meeting.update_from_form(form)
        meeting_render.f2m(meeting,form)
        meeting.register = current_user.id
        meeting.register_time = datetime.now()
        meeting.status = MeetingStatusType.REGISTERED
        try:
            db.session.add(meeting)
            db.session.commit()
            flash(_('提交成功，请等待管理员审核'))
            return redirect(url_for("meeting_detail", id=meeting.id))
        except sqlalchemy.exc.IntegrityError as e:
            flash(_('提交失败，请检查信息是否完整'))

    return render_template('registerMeeting.html', form=form, action='/register_meeting')


@app.route('/update_meeting_form', methods=['get', 'post'])
@user_required
@login_redirect_required
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
    # form = RegisterMeetingForm(
    #     title=meeting.title,
    #     title_EN = meeting.title_EN,
    #     location=meeting.full_location(),
    #     location_EN=meeting.full_location_EN(),
    #     start_date=meeting.start_date,
    #     end_date=meeting.end_date,
    #     lang=MeetingLanguageType.to_int(meeting.lang),
    #     theme = meeting.theme,
    #     theme_EN=meeting.theme_EN,
    #     url=meeting.url,
    #     key_words=meeting.key_words,
    #     short_name=meeting.short_name,
    #     contact=meeting.contact,
    #     email=meeting.email,
    #     phone=meeting.phone,
    # )
    form = RegisterMeetingForm()
    if form.validate_on_submit():

        meeting = Meeting.query.get(id)

        meeting.register = current_user.id
        meeting.register_time = datetime.now()
        meeting.status = MeetingStatusType.REGISTERED
        # meeting.update_from_form(form)
        meeting_render.f2m(meeting,form)
        db.session.commit()
        flash(_("修改成功，等待管理员再次审核"))
        return redirect(url_for("meeting_detail", id=meeting.id))
    else:
        meeting_render.m2f(meeting, form)  # 从meeting填入form
        return render_template('registerMeeting.html', form=form, action=url_for('update_meeting_form', id=id))


# 根据条件查询会议列表
def query_meetings(**conditions):
    '''

    :param conditions: start_date,end_date,status,register,keywords,lang,order_by
    :return:
    '''
    start_date = conditions.get('start_date')

    # 建立query
    query = Meeting.query

    # 处理开始时间
    if start_date:
        query = query.filter(Meeting.start_date >= start_date)
    else:
        query = query.filter(
            or_(
                Meeting.start_date == None,
                Meeting.start_date >= date.today()
            )
        )

    # 处理end_date
    end_date = conditions.get('end_date')
    if end_date:
        query = query.filter(Meeting.end_date <= end_date)

    # 处理status
    # 如果是管理员，则读取该参数，否则用approved
    status = conditions.get('status', 'APPROVED') \
        #           if current_user.is_authenticated and current_user.role == RoleType.ADMIN else \
    #          'APPROVED'

    query = query.filter(Meeting.status == MeetingStatusType.__members__[status])

    # 处理 register
    register = conditions.get('register')
    if register:
        query = query.filter(Meeting.register == register)

    # 处理search_keywords
    search_keywords = conditions.get('keywords', "")
    if search_keywords != "":
        search_keywords = "%{}%".format(search_keywords)
        query = query.filter(or_(
            Meeting.title.ilike(search_keywords),
            Meeting.title_EN.ilike(search_keywords),
            Meeting.theme.ilike(search_keywords),
            Meeting.theme_EN.ilike(search_keywords),
            Meeting.key_words.ilike(search_keywords),
            Meeting.key_words_EN.ilike(search_keywords),
            Meeting.short_name.ilike(search_keywords)
        ))
    # 处理语言
    lang = conditions.get('lang')
    if lang:
        query = query.filter(Meeting.lang == lang)

    # 处理排序方式
    order_by = conditions.get('order_by',Meeting.start_date)
    query = query.order_by(order_by)

    all_meetings = query.all()

    return all_meetings


@app.route("/meetings_year/<int:year>")
def meetings_year(year):
    title = _("{}年会议").format(year)
    meeting_list = query_meetings(start_date=date(year,1,1),end_date=date(year,12,31))
    return render_template('meetings.html', title=title, meetings=meeting_list,show_filter=True)


@app.route("/meetings", methods=['get', 'post'])
@login_redirect_required
def meetings():
    try:
        conditions = {}
        query_id = request.args.get('id')
        if query_id:
            return redirect(url_for('meeting_detail', id=query_id))
        start_date = request.args.get('start_date')

        # 处理　start_date
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            start_date = date.today()

        # query = Meeting.query.filter(Meeting.start_date >= start_date)
        conditions['start_date'] = start_date
        # 处理　end_date
        end_date = request.args.get('end_date')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            # query = query.filter(Meeting.start_date <= end_date)
            conditions['end_date'] = end_date

        # 处理status
        # 如果是管理员，则读取该参数，否则用approved
        status = request.args.get('status', 'APPROVED') \
            #           if current_user.is_authenticated and current_user.role == RoleType.ADMIN else \
        #          'APPROVED'

        # query = query.filter(Meeting.status == MeetingStatusType.__members__[status])
        conditions['status'] = status

        # 处理 register
        register = request.args.get('register')
        if register:
            # query = query.filter(Meeting.register == register)
            conditions['register'] = register
        # 处理search_keywords
        search_keywords = request.args.get('key_words')
        if search_keywords:
            search_keywords = "%{}%".format(search_keywords)
            # query = query.filter(or_(
            #     Meeting.title.ilike(search_keywords),
            #     Meeting.title_EN.ilike(search_keywords),
            #     Meeting.theme.ilike(search_keywords),
            #     Meeting.theme_EN.ilike(search_keywords),
            #     Meeting.key_words.ilike(search_keywords),
            #     Meeting.key_words_EN.ilike(search_keywords),
            #     Meeting.short_name.ilike(search_keywords)
            # ))
            conditions['keywords'] = search_keywords

        # all_meetings = query.order_by(Meeting.start_date).all()
        all_meetings = query_meetings(**conditions)
        return render_template('meetings.html', meetings=all_meetings, show_filter=False)



    except ValueError as e:
        return redirect(url_for('error', message='请求参数无效，请检查日期是否存在' + e))




@app.route("/meetingInfo/<int:id>")
@login_redirect_required
def meeting_detail(id):
    meeting = Meeting.query.get(id)
    if not meeting:
        return redirect(url_for('error', message='会议不存在'))
    register = User.query.get(meeting.register)
    return render_template('meeting_detail.html', meeting=meeting, register=register)


@app.route("/search_meeting_id")
def search_meeting_id():
    return render_template("search_meeting_id.html")


@app.route("/search_meeting", methods=['get', 'post'])
def search_meetings():
   
    form = SearchMeetingForm()

    return render_template("search_meetings.html", form=form)


@app.route("/new_meeting")
def new_meeting():
    title = _("新收录会议")
    meeting_list = query_meetings(order_by=desc(Meeting.register_time))
    return render_template('meetings.html', title=title, meetings=meeting_list,show_filter=True)

# @app.route("/search_meeting")
# @login_redirect_required
# def search_meeting():
#    return render_template("search_meeting.html")
