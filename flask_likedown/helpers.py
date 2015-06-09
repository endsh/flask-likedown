# coding: utf-8
from markdown import Markdown
from markdown.extensions.codehilite import makeExtension as code_extension
from .extensions import table_extension, toc_extension


def get_markdown():
    return Markdown(extensions=[
        table_extension(cls='table table-bordered'),
        toc_extension(cls='nav'),
        code_extension(),
        'markdown.extensions.abbr',
        'markdown.extensions.def_list',
        'markdown.extensions.fenced_code',
        'markdown.extensions.footnotes',
        'markdown.extensions.smart_strong',
    ])
