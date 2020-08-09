"""Набор задач для проекта."""
import requests
from bs4 import BeautifulSoup

from parse.celery import application

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


@application.task
def parse_site(site_url: str):
    """Парсинг указанного сайта."""
    site_response = requests.get(site_url)
    site_content = site_response.content.decode()
    document_node = BeautifulSoup(markup=site_content, features='html')

    # TODO: Возможна слишком большая нагрузка для большого дерева и бОльшего количества
    #   уровней; можно оптимизировать.
    nodes = _get_limited_depth_nodes(document_node, level=3)

    return site_url
