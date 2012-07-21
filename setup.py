#!/usr/bin/env python3

from distutils.core import setup

data_files = [
    ('/usr/bin', ['bin/accelerando'])
]
if True:
    data_files = []

setup(
    name='accelerando',
    version='0.1',
    description='Web Application Server supports Python3, PEP3333',
    author='Dong-seob Park',
    author_email='dongseob.park@gmail.com',
    url='http://github.com/Dongseob-Park/accelerando',
    package_dir={'': 'lib'},
    packages=['accelerando', 'accelerando.auth', 'accelerando.auth.digest', 'accelerando.session'],
    data_files=data_files
)
