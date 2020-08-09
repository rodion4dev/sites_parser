"""Набор задач для проекта."""
import tarfile
from shutil import copyfileobj
from typing import List

import requests
from bs4 import BeautifulSoup
from celery import Task
from requests import HTTPError

from parse.celery import Config, application

LATEST_ELEMENT_INDEX = -1


def _get_limited_depth_nodes(node: BeautifulSoup, level: int = 1):
    """
    Складирование элементов дерева (и вложенных в него) одного уровня в один список.

    :param level: Лимитирование глубины.
    :param node: Корневой элемент дерева, с которого начинается обход.
    """
    depths = [[node]]
    for _ in range(level):
        one_depth_nodes = depths[LATEST_ELEMENT_INDEX]
        next_depth_nodes = []
        for node in one_depth_nodes:
            next_depth_nodes.extend(node.find_all(recursive=False))
        depths.append(next_depth_nodes)
    return depths


def _find_file_urls(node: BeautifulSoup) -> List[str]:
    """Поиск путей к файлам из указанного элемента дерева."""
    return ['']


@application.task(bind=True)
def parse_site(current_task: Task, site_url: str):
    """Парсинг указанного сайта."""
    site_response = requests.get(site_url)
    site_content = site_response.content.decode()
    document_node = BeautifulSoup(markup=site_content, features='html')

    # TODO: Возможна слишком большая нагрузка для большого дерева и бОльшего количества
    #   уровней; можно оптимизировать.
    nodes = _get_limited_depth_nodes(document_node, level=3)
    file_urls = []
    for one_depth_nodes in nodes:
        for node in one_depth_nodes:
            file_urls.extend(_find_file_urls(node))

    task_directory = Config.MEDIA_ROOT_PATH / current_task.request.id
    task_directory.mkdir(mode=0o755)
    for file_url in file_urls:
        local_filename = file_url.split('/')[LATEST_ELEMENT_INDEX]
        with requests.get(file_url, stream=True) as response:
            try:
                response.raise_for_status()
            except HTTPError:
                continue

            with (task_directory / local_filename).open(mode='wb') as file:
                copyfileobj(response.raw, file)

    with tarfile.open(Config.MEDIA_ROOT_PATH / current_task.request.id, 'w:gz') as tar:
        for file in task_directory.iterdir():
            tar.add(file.name)

    return site_url
