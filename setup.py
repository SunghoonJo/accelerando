#!/usr/bin/env python3

from distutils.core import setup

setup(
		name='accelerando',
		version='0.1',
		description='Web Application Server supports Python3, PEP3333',
		author='Dong-seob Park',
		author_email='dongseob.park@gmail.com',
		url='http://github.com/Dongseob-Park/accelerando',
		package_dir={'': 'src'},
		packages=['accelerando', 'accelerando.dispatcher', 'accelerando.processor'],
		data_files=[
			('/usr/bin', ['bin/accel'])
		]
)
