from tasks_call.celery import application


@application.task
def parse_site(site_url: str):
    """Парсинг указанного сайта."""
    return site_url
