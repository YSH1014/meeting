from app import app
import getpass
from app import db
from app.models import User,RoleType
print("该脚本用于建立root用户")

email = input("输入邮箱")
password  = getpass.win_getpass("输入密码")
phone = input("输入手机号")
root = User(
    username='root',
    email=email,
    phone = phone,
    address='ROOT'
)
root.set_password(password)
root.set_role(RoleType.ROOT)

db.session.add(root)
db.session.commit()