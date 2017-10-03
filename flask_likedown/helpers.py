# coding: utf-8
from markdown import Markdown
from .extensions import table_extension, toc_extension, code_extension


def get_markdown():
    return Markdown(extensions=[
        table_extension(cls='table table-bordered'),
        toc_extension(cls='nav'),
        code_extension(use_pygments=False),
        'markdown.extensions.abbr',
        'markdown.extensions.def_list',
        'markdown.extensions.fenced_code',
        'markdown.extensions.footnotes',
        'markdown.extensions.smart_strong',
    ])
