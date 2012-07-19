#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='accelerando',
    version='0.1',
    description='Web Application Server supports Python3, PEP3333',
    author='Dong-seob Park',
    author_email='dongseob.park@gmail.com',
    url='http://github.com/Dongseob-Park/accelerando',
    package_dir={'': 'lib'},
    packages=['wsgi', 'wsgi.auth', 'wsgi.auth.digest', 'wsgi.session'],
    data_files=[
        ('/usr/bin', ['bin/wsgiup'])
        ]
)
