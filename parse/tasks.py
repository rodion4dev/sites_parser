"""Набор задач для проекта."""
import tarfile
from pathlib import Path
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

    # TODO: Возможна слишком большая нагрузка для большого дерева и бОльшего количества
    #   уровней; можно оптимизировать.

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


def _get_file_urls_from_site_content(site_content: str):
    document_node = BeautifulSoup(markup=site_content, features='html')
    nodes = _get_limited_depth_nodes(document_node, level=3)
    file_urls = []
    for one_depth_nodes in nodes:
        for node in one_depth_nodes:
            file_urls.extend(_find_file_urls(node))
    return file_urls


def _download_files(file_urls: List[str], directory: Path) -> List[str]:
    """Загрузка файлов по указанным ссылкам."""
    file_paths = []
    for file_url in file_urls:
        local_filename = file_url.split('/')[LATEST_ELEMENT_INDEX]
        with requests.get(file_url, stream=True) as response:
            try:
                response.raise_for_status()
            except HTTPError:
                continue

            with (directory / local_filename).open(mode='wb') as file:
                copyfileobj(response.raw, file)
        file_paths.append(str(directory / local_filename))
    return file_paths


@application.task(bind=True)
def parse_site(current_task: Task, site_url: str):
    """Парсинг указанного сайта."""
    try:
        site_response = requests.get(site_url)
        site_response.raise_for_status()
        site_content = site_response.content.decode()
    except HTTPError as error:
        return str(error)

    file_urls = _get_file_urls_from_site_content(site_content)
    task_directory = Config.MEDIA_ROOT_PATH / current_task.request.id
    task_directory.mkdir(mode=0o755)
    file_paths = _download_files(file_urls, task_directory)

    with tarfile.open(Config.MEDIA_ROOT_PATH / current_task.request.id, 'w:gz') as tar:
        for file_name in file_paths:
            tar.add(file_name)

    return task_directory.absolute()
