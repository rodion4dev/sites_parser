import os


class _Config:
    DEBUG: bool = os.environ.get('DEBUG', default='False').lower() == 'true'
    SECRET_KEY: str = os.environ['SECRET_KEY']
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


config = _Config()
