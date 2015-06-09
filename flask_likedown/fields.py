# coding: utf-8
from wtforms.fields import StringField
from .widgets import LikedownInput
from .helpers import get_markdown


class LikedownField(StringField):

    widget = LikedownInput()

    def __init__(self, label, show_modals=True, **kwargs):
        super(LikedownField, self).__init__(label, **kwargs)
        self.show_modals = show_modals

    def markdown(self):
        self._markdown = get_markdown()
        self._html = self._markdown.convert(self._value())
        self._toc = self._markdown.toc

    @property
    def html(self):
        if not hasattr(self, '_html'):
            self.markdown()
        return self._html

    @property
    def toc(self):
        if not hasattr(self, '_toc'):
            self.markdown()
        return self._toc