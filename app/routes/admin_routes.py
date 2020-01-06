from app import app
from app import db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting
import sqlalchemy.exc
from app.security import admin_required


@admin_required
@app.route('/approve/<int:id>')
def approve(id):
    meeting = Meeting.query.get(id)
    meeting.status = MeetingStatusType.APPROVED
    db.session.commit()
    return redirect(url_for('meetingInfo',id=id))

@admin_required
@app.route('/unapprove/<int:id>')
def unapprove(id):
    meeting = Meeting.query.get(id)
    meeting.status = MeetingStatusType.UNAPPROVED
    db.session.commit()
    return redirect(url_for('meetingInfo', id=id))
