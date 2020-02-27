from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from tools.ModelFormRender import ModelFormRender
from flask_babelex import Babel


app = Flask(__name__)
load_dotenv('.flaskenv')
load_dotenv('.env')
from app.config import Config
app.config.from_object(Config)

#加载flask插件
login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
babel = Babel(app)

from app.cli import register_commands
register_commands(app)

# 环境相关文件
from app import index_routes, models
if app.config['ENV']!='development':
    from app.routes import login_production
else :
    from app.routes import login_development
from app.routes import  admin_routes,meeting_routes,root_routes,user_routes

from app.index_routes import get_locale
app.jinja_env.globals['get_locale'] = get_locale