import os

from celery import Celery


class Config:
    CELERY_BROKER: str = os.environ.get('CELERY_BROKER')
    CELERY_BROKER_HOST: str = os.environ.get('CELERY_BROKER_HOST')
    CELERY_BROKER_PORT: str = os.environ.get('CELERY_BROKER_PORT')
    CELERY_BROKER_VIRTUAL_HOST: str = os.environ.get(
        'CELERY_BROKER_VIRTUAL_HOST')
    CELERY_RESULTS_BACKEND: str = os.environ.get('CELERY_RESULTS_BACKEND')
    CELERY_RESULTS_BACKEND_HOST: str = os.environ.get(
        'CELERY_RESULTS_BACKEND_HOST')
    CELERY_RESULTS_BACKEND_PORT: str = os.environ.get(
        'CELERY_RESULTS_BACKEND_PORT')
    CELERY_RESULTS_BACKEND_VIRTUAL_HOST: str = os.environ.get(
        'CELERY_RESULTS_BACKEND_VIRTUAL_HOST')


broker_url_template = ('{transport}://{userid}:{password}@{hostname}:'
                       '{port}/{virtual_host}')
backend_url_template = broker_url_template

broker = broker_url_template.format(
    transport=Config.CELERY_BROKER, userid='', password='',
    hostname=Config.CELERY_BROKER_HOST, port=Config.CELERY_BROKER_PORT,
    virtual_host=Config.CELERY_BROKER_VIRTUAL_HOST)
backend = backend_url_template.format(
    transport=Config.CELERY_RESULTS_BACKEND, userid='', password='',
    hostname=Config.CELERY_RESULTS_BACKEND_HOST,
    port=Config.CELERY_RESULTS_BACKEND_PORT,
    virtual_host=Config.CELERY_RESULTS_BACKEND_VIRTUAL_HOST)

application = Celery(main='tasks_call', backend=backend, broker=broker,
                     include=['tasks_call.tasks'])
