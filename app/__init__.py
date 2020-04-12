from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from flask_babelex import Babel
from flask_admin import Admin

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
admin = Admin(app)

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

# 日志记录
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
import logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
# initialize the log handler
loggerHandler: RotatingFileHandler = RotatingFileHandler('flask.logs', maxBytes=1000, backupCount=1)
app.logger.addHandler(loggerHandler)
