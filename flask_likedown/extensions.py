# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.extensions.toc import slugify
from markdown.extensions.toc import TocTreeprocessor as _TocTreeprocessor
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree


class TableProcessor(BlockProcessor):
    """ Process Tables. """

    def __init__(self, parser, cls=None):
        BlockProcessor.__init__(self, parser)
        self.cls = cls

    def test(self, parent, block):
        rows = block.split('\n')
        return (len(rows) > 1 and '|' in rows[0] and
                '|' in rows[1] and '-' in rows[1] and
                rows[1].strip()[0] in ['|', ':', '-'])

    def run(self, parent, blocks):
        """ Parse a table block and build table. """
        block = blocks.pop(0).split('\n')
        header = block[0].strip()
        seperator = block[1].strip()
        rows = [] if len(block) < 3 else block[2:]
        # Get format type (bordered by pipes or not)
        border = False
        if header.startswith('|'):
            border = True
        # Get alignment of columns
        align = []
        for c in self._split_row(seperator, border):
            if c.startswith(':') and c.endswith(':'):
                align.append('center')
            elif c.startswith(':'):
                align.append('left')
            elif c.endswith(':'):
                align.append('right')
            else:
                align.append(None)

        # Build table
        attrs = {'class':self.cls} if self.cls else {}
        table = etree.SubElement(parent, 'table', attrs)
        thead = etree.SubElement(table, 'thead')
        self._build_row(header, thead, align, border)
        tbody = etree.SubElement(table, 'tbody')
        for row in rows:
            self._build_row(row.strip(), tbody, align, border)

    def _build_row(self, row, parent, align, border):
        """ Given a row of text, build table cells. """
        tr = etree.SubElement(parent, 'tr')
        tag = 'td'
        if parent.tag == 'thead':
            tag = 'th'
        cells = self._split_row(row, border)
        # We use align here rather than cells to ensure every row
        # contains the same number of columns.
        for i, a in enumerate(align):
            c = etree.SubElement(tr, tag)
            try:
                c.text = cells[i].strip()
            except IndexError:  # pragma: no cover
                c.text = ""
            if a:
                c.set('align', a)

    def _split_row(self, row, border):
        """ split a row of text into list of cells. """
        if border:
            if row.startswith('|'):
                row = row[1:]
            if row.endswith('|'):
                row = row[:-1]
        return [x.strip() for x in row.split('|')]


class TableExtension(Extension):
    """ Add tables to Markdown. """

    def __init__(self, cls=None, **kwargs):
        super(Extension, self).__init__(**kwargs)
        self.cls = cls

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of TableProcessor to BlockParser. """
        md.parser.blockprocessors.add('table',
            TableProcessor(md.parser, self.cls), '<hashheader')


class TocTreeprocessor(_TocTreeprocessor):

    def __init__(self, md, config):
        super(TocTreeprocessor, self).__init__(md, config)
        self.cls = config["cls"]

    def build_toc_div(self, toc_list):
        """ Return a string div given a toc list. """
        div = etree.Element("div")
        div.attrib["class"] = "toc"

        # Add title to the div
        if self.title:
            header = etree.SubElement(div, "span")
            header.attrib["class"] = "toctitle"
            header.text = self.title

        def build_etree_ul(toc_list, parent, cls=None):
            attrs = {'class':cls} if cls else {}
            ul = etree.SubElement(parent, "ul", attrs)
            for item in toc_list:
                # List item link, to be inserted into the toc div
                li = etree.SubElement(ul, "li")
                link = etree.SubElement(li, "a")
                link.text = item.get('name', '')
                link.attrib["href"] = '#' + item.get('id', '')
                if item['children']:
                    build_etree_ul(item['children'], li)
            return ul

        bg = etree.SubElement(div, 'div', {'class':'toc-active-bg'})

        build_etree_ul(toc_list, div, self.cls)
        prettify = self.markdown.treeprocessors.get('prettify')
        if prettify:
            prettify.run(div)
        return div


class TocExtension(Extension):

    TreeProcessorClass = TocTreeprocessor

    def __init__(self, *args, **kwargs):
        self.config = {
            "marker": ['[TOC]',
                       'Text to find and replace with Table of Contents - '
                       'Set to an empty string to disable. Defaults to "[TOC]"'],
            "title": ["",
                      "Title to insert into TOC <div> - "
                      "Defaults to an empty string"],
            "anchorlink": [False,
                           "True if header should be a self link - "
                           "Defaults to False"],
            "permalink": [0,
                          "True or link text if a Sphinx-style permalink should "
                          "be added - Defaults to False"],
            "baselevel": ['1', 'Base level for headers.'],
            "slugify": [slugify,
                        "Function to generate anchors based on header text - "
                        "Defaults to the headerid ext's slugify function."],
            'separator': ['-', 'Word separator. Defaults to "-".'],
            'cls': ['', 'ul class']
        }

        super(TocExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        self.md = md
        self.reset()
        tocext = self.TreeProcessorClass(md, self.getConfigs())
        md.treeprocessors.add("toc", tocext, "_end")

    def reset(self):
        self.md.toc = ''


class CodeExtension(CodeHiliteExtension):
    pass


def table_extension(*args, **kwargs):
    return TableExtension(*args, **kwargs)


def toc_extension(*args, **kwargs):
    return TocExtension(*args, **kwargs)


def code_extension(*args, **kwargs):
    return CodeExtension(*args, **kwargs)
