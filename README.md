Flask-Likedown
==============

It is a markdown eidtor based on [likedown.js][1] and [WTForms][2]. 

For more information see: http://flask-likedown.chiki.org

Simple usage
------------

```python
# coding: utf-8
from flask import Flask, request, render_template
from flask.ext.likedown import LikedownField
from wtforms.form import Form
from wtforms.fields import TextField

app = Flask(__name__)

class EntryForm(Form):
    title = TextField("标题")
    content = LikedownField("正文")

@app.route('/', methods=('GET', 'POST'))
def index():
    form = EntryForm(request.form)
    if request.method == 'POST':
        context = dict(
            title=form.title.data, 
            content=form.content.html,
            toc=form.content.toc,
        )
        return render_template('post.html', **context)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
```

  [1]: https://github.com/endsh/likedown
  [2]: https://github.com/wtforms/wtforms