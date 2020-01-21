from app import app
from app import db
from app.models import User, RoleType

u = User(username='root', email='123@abc.com', address='aaa', phone='aaa',role=RoleType.ROOT)
u.set_password('aaa')
db.session.add(u)
db.session.commit()
