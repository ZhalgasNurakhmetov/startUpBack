import os

from pydantic import BaseSettings


class DevelopmentSettings(BaseSettings):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    START_UP_KEY: str = os.getenv('START_UP_KEY')
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URI')
    MAIL_SERVER: str = os.getenv('MAIL_SERVER')
    MAIL_PORT: str = os.getenv('MAIL_PORT')
    MAIL_USERNAME: str = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD')


settings = DevelopmentSettings()
