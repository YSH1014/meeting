from app import app
from app import db
from app.models import User

u = User(username='aaa',email='',address='',phone='')
u.set_password('aaa')
db.session.add(u)
db.session.commit()