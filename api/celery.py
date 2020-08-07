from celery import Celery

from api.settings import config

broker_url_template = ('{transport}://{userid}:{password}@{hostname}:'
                       '{port}/{virtual_host}')
broker = broker_url_template.format(
    transport=config.CELERY_BROKER, userid='', password='',
    hostname=config.CELERY_BROKER_HOST, port=config.CELERY_BROKER_PORT,
    virtual_host=config.CELERY_BROKER_VIRTUAL_HOST)

application = Celery(main='tasks', broker=broker)
