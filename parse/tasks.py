"""Набор задач для проекта."""
import re
import tarfile
from pathlib import Path
from shutil import copyfileobj, rmtree
from typing import List, Optional

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


def _find_file_url(node: BeautifulSoup) -> Optional[str]:
    """
    Поиск путей к файлам из указанного элемента дерева.

    TODO: Не совсем корректный вариант поиска; окончание ссылки на filename.extension
        не говорит о том, что в качестве ответа вернётся файл.
    """
    file_suffixes = '|'.join(Config.PARSE_FILE_SUFFIXES)
    file_suffixes_group = rf'({file_suffixes})'
    is_file_url_pattern = re.compile(rf'^https?://\S*\.{file_suffixes_group}$')

    if node.name in ['img', 'script']:
        source = node.attrs.get('src', '')
        is_file_url = is_file_url_pattern.match(source)
        return source if is_file_url else None
    elif node.name in ['link', 'a']:
        href = node.attrs.get('href', default='')
        is_file_url = is_file_url_pattern.match(href)
        return href if is_file_url else None
    elif not node.name:
        is_file_url = is_file_url_pattern.match(node.title)
        return node.title if is_file_url else None


def _get_file_urls_from_site_content(site_content: str) -> List[str]:
    """Получение ссылок до любых файлов из указанного содержимого."""
    document_node = BeautifulSoup(markup=site_content, features='html.parser')
    nodes = _get_limited_depth_nodes(document_node, level=3)
    file_urls = []
    for one_depth_nodes in nodes:
        for node in one_depth_nodes:
            file_urls.append(_find_file_url(node))
    return list(filter(None, file_urls))


def _download_files(file_urls: List[str], directory: Path):
    """
    Загрузка файлов по указанным ссылкам.

    :param file_urls: Ссылки до загружаемых файлов.
    :param directory: Директория, в которой располагаются загружаемые файлы.
    """
    for file_url in file_urls:
        local_filename = file_url.split('/')[LATEST_ELEMENT_INDEX]
        with requests.get(file_url, stream=True) as response:
            try:
                response.raise_for_status()
            except HTTPError:
                continue

            with (directory / local_filename).open(mode='wb') as file:
                copyfileobj(response.raw, file)


def _parse_site(site_url: str, storage_name: str) -> Optional[str]:
    """Парсинг указанного сайта."""
    try:
        site_response = requests.get(site_url)
        site_response.raise_for_status()
        site_content = site_response.content.decode()
    except HTTPError as error:
        return str(error)

    storage_path = Config.MEDIA_ROOT_PATH / storage_name
    storage_path.mkdir(mode=0o755)

    file_urls = _get_file_urls_from_site_content(site_content)
    _download_files(file_urls, storage_path)

    archive_url = None
    if list(storage_path.iterdir()):
        archive_path = Config.MEDIA_ROOT_PATH / f'{storage_name}.tar.gz'
        with tarfile.open(str(archive_path), 'w:gz') as archive:
            archive.add(str(storage_path.absolute()), arcname=storage_name)
        archive_url = Config.FILES_PROXY_RESOURCE + archive_path.name

    rmtree(str(storage_path))
    return archive_url


@application.task(bind=True)
def parse_site(current_task: Task, site_url: str) -> str:
    """Celery задача для парсинга сайта."""
    return _parse_site(site_url, str(current_task.request.id))
