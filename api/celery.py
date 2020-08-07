from celery import Celery

from api.settings import config

redis_url_template = 'redis://{host}:{port}/{database_number}'
redis_broker = redis_url_template.format(
    host=config.REDIS_HOST, port=config.REDIS_PORT,
    database_number=config.REDIS_BROKER_DATABASE_NUMBER)
redis_backend = redis_url_template.format(
    host=config.REDIS_HOST, port=config.REDIS_PORT,
    database_number=config.REDIS_RESULTS_DATABASE_NUMBER)
application = Celery(main='tasks', broker=redis_broker, backend=redis_backend)
