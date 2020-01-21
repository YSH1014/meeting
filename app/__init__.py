from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv


app = Flask(__name__)


load_dotenv('.flaskenv')

load_dotenv('.env')


from app.config import Config
app.config.from_object(Config)

login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import index_routes, models
from app.routes import user_routes,admin_routes,meeting_routes,root_routes

