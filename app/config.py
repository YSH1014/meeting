import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    POSTGRES_URL = os.environ.get("POSTGRES_URL")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PW = os.environ.get("POSTGRES_PW")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = ( \
        (os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'app.db')))  # 开发模式使用sqlite
        if os.environ.get('FLASK_ENV') == 'development' \
            else 'postgresql+psycopg2://{user}:{pw}@{url}/{db}' \
            .format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB) #否则使用postgre
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
