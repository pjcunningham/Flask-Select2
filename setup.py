# coding: utf-8
__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2017, Paul Cunningham'

import os
import re
from setuptools import setup, find_packages

DIRECTORY_NAME = os.path.dirname(__file__)
rel = lambda *parts: os.path.abspath(os.path.join(DIRECTORY_NAME, *parts))

with open(rel('flask_select2', '__init__.py')) as handler:
    INIT_PY = handler.read()

INSTALL_REQUIRES = [
    'Flask>=0.7',
    'wtforms'
]


VERSION = re.findall("__version__ = '([^']+)'", INIT_PY)[0]
AUTHOR = re.findall("__author__ = '([^']+)'", INIT_PY)[0]
EMAIL = re.findall("__email__ = '([^']+)'", INIT_PY)[0]
LICENSE = re.findall("__license__ = '([^']+)'", INIT_PY)[0]

setup(
    name='Flask-Select2',
    packages=find_packages(),
    include_package_data=True,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    install_requires=INSTALL_REQUIRES,
    platforms='any',
    description='Flask integration with Select2.js',
    url='https://github.com/pjcunningham/Flask-Select2',
    keywords=['flask', 'select2'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    license=LICENSE,
)
