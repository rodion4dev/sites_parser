import os

from celery import Celery


class _CeleryBrokerConfig:
    """Celery конфигурация для брокера."""

    CELERY_BROKER: str = os.environ.get('CELERY_BROKER')
    CELERY_BROKER_HOST: str = os.environ.get('CELERY_BROKER_HOST')
    CELERY_BROKER_PORT: str = os.environ.get('CELERY_BROKER_PORT')
    CELERY_BROKER_VIRTUAL_HOST: str = os.environ.get('CELERY_BROKER_VIRTUAL_HOST')


class _CeleryResultsBackendConfig:
    """Celery конфигурация для базы данных с результатами."""

    CELERY_RESULTS_BACKEND: str = os.environ.get('CELERY_RESULTS_BACKEND')
    CELERY_RESULTS_BACKEND_HOST: str = os.environ.get('CELERY_RESULTS_BACKEND_HOST')
    CELERY_RESULTS_BACKEND_PORT: str = os.environ.get('CELERY_RESULTS_BACKEND_PORT')
    CELERY_RESULTS_BACKEND_VIRTUAL_HOST: str = os.environ.get(
        'CELERY_RESULTS_BACKEND_VIRTUAL_HOST'
    )


class Config(_CeleryBrokerConfig, _CeleryResultsBackendConfig):
    """Общая конфигурация проекта."""


broker_url_template = (
    '{transport}://{userid}:{password}@{hostname}:' '{port}/{virtual_host}'
)
backend_url_template = broker_url_template

broker = broker_url_template.format(
    transport=Config.CELERY_BROKER,
    userid='',
    password='',
    hostname=Config.CELERY_BROKER_HOST,
    port=Config.CELERY_BROKER_PORT,
    virtual_host=Config.CELERY_BROKER_VIRTUAL_HOST,
)
backend = backend_url_template.format(
    transport=Config.CELERY_RESULTS_BACKEND,
    userid='',
    password='',
    hostname=Config.CELERY_RESULTS_BACKEND_HOST,
    port=Config.CELERY_RESULTS_BACKEND_PORT,
    virtual_host=Config.CELERY_RESULTS_BACKEND_VIRTUAL_HOST,
)

application = Celery(
    main='parse_execute',
    backend=backend,
    broker=broker,
    include=['parse_execute.tasks'],
)