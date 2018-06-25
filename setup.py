# coding: utf-8
import re
from os import path
from setuptools import setup

version_file = path.join(
    path.dirname(__file__), 'flask_validate', '__version__.py')
with open(version_file, 'r') as fp:
    m = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", fp.read(), re.M)
    version = m.groups(1)[0]

setup(
    name='Flask-Validate',
    version=version,
    author='zhangguangchao',
    description='A request validator for Flask, including information in headers, query_string and request body.',
    author_email='zhangguangchao@youzan.com',
    packages=['flask_validate'],
    install_requires=['WTForms==2.1', 'Flask==1.0.2', 'jsonschema==2.6.0'],
    package_data={'cloudcli': ['resources/*']},
    classifiers=[
        'Framework :: Flask',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ])
