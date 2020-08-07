import os

from celery import Celery


class Config:
    REDIS_HOST: str = os.environ.get('REDIS_HOST')
    REDIS_PORT: int = int(os.environ.get('REDIS_PORT', default='6379'))
    REDIS_BROKER_DATABASE_NUMBER: int = int(
        os.environ.get('REDIS_BROKER_DATABASE_NUMBER', default='0'))


redis_url_template = 'redis://{host}:{port}/{database_number}'
redis_broker = redis_url_template.format(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT,
    database_number=Config.REDIS_BROKER_DATABASE_NUMBER)
application = Celery(main='tasks_call', broker=redis_broker,
                     include=['tasks_call.tasks'])
