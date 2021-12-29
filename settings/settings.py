import os

from pydantic import BaseSettings


class DevelopmentSettings(BaseSettings):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY: str = os.getenv('START_UP_KEY')
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_WEEKS: int = 1
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URL')
    MAIL_SERVER: str = os.getenv('MAIL_SERVER')
    MAIL_PORT: str = os.getenv('MAIL_PORT')
    MAIL_USERNAME: str = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD')


settings = DevelopmentSettings()
