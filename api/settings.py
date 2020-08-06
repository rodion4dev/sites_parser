import os


class Config:
    DEBUG: bool = os.environ.get('DEBUG', default='False').lower() == 'true'
    SECRET_KEY: str = os.environ['SECRET_KEY']


config = Config()
