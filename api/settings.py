import os


class _Config:
    DEBUG: bool = os.environ.get('DEBUG', default='False').lower() == 'true'
    SECRET_KEY: str = os.environ['SECRET_KEY']
    REDIS_HOST: str = os.environ.get('REDIS_HOST')
    REDIS_PORT: int = int(os.environ.get('REDIS_PORT', default='6379'))
    REDIS_BROKER_DATABASE_NUMBER: int = int(
        os.environ.get('REDIS_BROKER_DATABASE_NUMBER', default='0'))
    REDIS_RESULTS_DATABASE_NUMBER: int = int(
        os.environ.get('REDIS_RESULTS_DATABASE_NUMBER', default='0'))


config = _Config()
