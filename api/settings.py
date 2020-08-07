"""Модуль с настройками проекта."""
import os


class _CeleryBrokerConfig:
    """Настройки Celery брокера."""

    CELERY_BROKER: str = os.environ.get('CELERY_BROKER')
    CELERY_BROKER_HOST: str = os.environ.get('CELERY_BROKER_HOST')
    CELERY_BROKER_PORT: str = os.environ.get('CELERY_BROKER_PORT')
    CELERY_BROKER_VIRTUAL_HOST: str = os.environ.get('CELERY_BROKER_VIRTUAL_HOST')


class _CeleryResultsBackendConfig:
    """Настройки Celery сервиса для хранения результатов."""

    CELERY_RESULTS_BACKEND: str = os.environ.get('CELERY_RESULTS_BACKEND')
    CELERY_RESULTS_BACKEND_HOST: str = os.environ.get('CELERY_RESULTS_BACKEND_HOST')
    CELERY_RESULTS_BACKEND_PORT: str = os.environ.get('CELERY_RESULTS_BACKEND_PORT')
    CELERY_RESULTS_BACKEND_VIRTUAL_HOST: str = os.environ.get(
        'CELERY_RESULTS_BACKEND_VIRTUAL_HOST'
    )


class _Config(_CeleryBrokerConfig, _CeleryResultsBackendConfig):
    """Класс настроек проекта."""

    DEBUG: bool = os.environ.get('DEBUG', default='False').lower() == 'true'
    SECRET_KEY: str = os.environ['SECRET_KEY']


config = _Config()
