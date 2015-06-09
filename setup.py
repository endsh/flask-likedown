# coding: utf-8
import re
from setuptools import setup

with open('flask_likedown/__init__.py') as f:
    m = re.findall(r'__version__\s*=\s*\'(.*)\'', f.read())
    version = m[0]


setup(
    name='Flask-Likedown',
    version=version,
    url='http://github.com/endsh/flask-likedown',
    license='BSD',
    author='Linshao',
    author_email='438985635@qq.com',
    description='A markdown editor of Flask and WTForms based on likedown.',
    packages=[
        'flask_likedown'
    ],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Werkzeug',
        'WTForms',
        'markdown',
    ]
)
