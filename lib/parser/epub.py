# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from epubzilla.epubzilla import Epub


def parse_structure(filepath):
    """
    解析 epub 文件结构并返回
    :param filepath: epub 路径
    :return: [{'chapter': 'name', 'identifier': 'Section.xhtml'}, ...]
    """
    structure = []
    epub = Epub.from_file(filepath)
    for item in epub.manifest.list:
        if item.tag.attributes.get('media-type') != 'application/xhtml+xml':
            continue
        identifier = item.tag.attributes.get('id', '')
        if not identifier:
            continue
        if len(_chapter_content(epub, identifier)) == 0:
            continue

        content_list = BeautifulSoup(item.get_file(), 'lxml').body.contents
        chapter = None
        for title in content_list:
            if type(title) in [str, NavigableString] and len(title.strip()) > 0:
                chapter = title
                break
            if type(title) == Tag:
                if title.name == 'p':
                    chapter = ''
                else:
                    chapter = ''.join(x for x in title.stripped_strings)
                break

        structure.append({
            'chapter': chapter,
            'identifier': identifier,
        })
    return structure


def chapter_content(filepath, identifier):
    """
    获取 epub 文件指定章节的内容
    :param filepath: epub 路径
    :param identifier: 章节标识符
    :return: ['段落1', '段落2', ...]
    """
    epub = Epub.from_file(filepath)
    return _chapter_content(epub, identifier)


def _chapter_content(epub, identifier):
    """
    内部函数
    :param epub: epub 文件  
    :param identifier: 章节标识符
    :return: ['段落1', '段落2', ...]
    """
    try:
        element = epub.manifest.getElementById(identifier)
    except Exception:
        return []
    body = BeautifulSoup(element.get_file(), 'lxml').body
    if not body or type(body) != Tag:
        return []

    contents = []
    for item in body.stripped_strings:
        contents.append(item)
    return contents
