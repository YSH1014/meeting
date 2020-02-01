from app import app
from app import db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm, RegisterMeetingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, load_user, RoleType, MeetingStatusType, Meeting
import sqlalchemy.exc
from app.security import admin_required, login_redirect_required
# from app import bp

@app.route('/approve/<int:id>')
@admin_required
@login_redirect_required
def approve(id):
    meeting = Meeting.query.get(id)
    meeting.status = MeetingStatusType.APPROVED
    db.session.commit()
    return redirect(url_for('meeting_detail',id=id))

@app.route('/unapprove/<int:id>')
@admin_required
@login_redirect_required
def unapprove(id):
    meeting = Meeting.query.get(id)
    meeting.status = MeetingStatusType.UNAPPROVED
    db.session.commit()
    return redirect(url_for('meeting_detail', id=id))
