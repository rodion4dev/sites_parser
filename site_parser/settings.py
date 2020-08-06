import os


class Config:
    DEBUG: bool = os.environ.get('DEBUG', default='False').lower() == 'true'
    SECRET_KEY: str = os.environ['SECRET_KEY']
    REDIS_DATABASE_HOSTNAME: str = os.environ.get('REDIS_DATABASE_HOSTNAME')
    REDIS_DATABASE_PORT: int = int(os.environ.get('REDIS_DATABASE_PORT'))
    REDIS_DATABASE_NUMBER: int = int(os.environ.get('REDIS_DATABASE_NUMBER',
                                                    default='0'))


config = Config()
