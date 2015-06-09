# coding: utf-8
from wtforms.widgets import html_params, HTMLString
from wtforms.compat import text_type


class LikedownInput(object):

    html_params = staticmethod(html_params)
    tpl = """
<div id="wmd-editor%(postfix)s" class="wmd-editor%(editor_class)s" data-postfix="%(postfix)s" data-type="likedown">
    <div id="wmd-button-bar%(postfix)s" class="wmd-button-bar"></div>
    <div class="wmd-input-box">
        <textarea id="wmd-input%(postfix)s" class="wmd-input form-control" name="%(name)s">%(value)s</textarea>
    </div>
    <div class="wmd-line"></div>
    <div class="wmd-preview-box">
        <div id="wmd-preview%(postfix)s" class="wmd-preview likedown"></div>
    </div>
</div>
"""
    modals = u"""<div class="modal fade modal-insert-link">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal"
                        aria-hidden="true">&times;</button>
                    <h4 class="modal-title">插入链接</h4>
                </div>
                <div class="modal-body">
                    <div class="input-group">
                        <span class="input-group-addon"><i class="glyphicon glyphicon-globe"></i></span>
                        <input id="input-insert-link" type="text" class="col-sm-5 form-control" 
                            placeholder='http://example.com/' />
                    </div>
                </div>
                <div class="modal-footer">
                    <a href="#" class="btn btn-default" data-dismiss="modal">取消</a>
                    <a href="#" class="btn btn-primary action-insert-link" data-dismiss="modal">插入</a>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade modal-insert-image">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal"
                        aria-hidden="true">&times;</button>
                    <h4 class="modal-title">插入图片</h4>
                </div>
                <div class="modal-body">
                    <div class="input-group">
                        <span class="input-group-addon"><i class="glyphicon glyphicon-picture"></i></span>
                        <input id="input-insert-image" type="text" class="col-sm-5 form-control"
                            placeholder='http://example.com/image.jpg' />
                    </div>
                </div>
                <div class="modal-footer">
                    <a href="#" class="btn btn-default" data-dismiss="modal">取消</a>
                    <a href="#" class="btn btn-primary action-insert-image" data-dismiss="modal">插入</a>
                </div>
            </div>
        </div>
    </div>
"""

    def __call__(self, field, **kwargs):
        postfix = kwargs.get('postfix', field.id)
        editor_class = kwargs.get('editor_class', 'live-mode')
        editor_class = ' ' + editor_class if editor_class else ''
        html = self.tpl % dict(
            name=field.name,
            postfix=postfix,
            editor_class=editor_class,
            value=text_type(field._value()),
        )
        if field.show_modals:
            html += self.modals
        return HTMLString(html)