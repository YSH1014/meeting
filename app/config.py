import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    POSTGRES_URL = os.environ.get("POSTGRES_URL")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PW = os.environ.get("POSTGRES_PW")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}' \
            .format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB) 
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'zh_Hans_CN']

    CAL_ADMIN=os.environ.get("CAL_ADMIN")
    #CAL_ADMIN="http://meeting:meeting@localhost:5232/meeting/"