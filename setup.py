#!/usr/bin/env python

from distutils.core import setup
from version import __version__

setup(name='dmrg_helpers',
		version=__version__,
        description='Python helpers from our main DMRG code',
		long_description=open('README.md').read(),
		author='Ivan Gonzalez',
		author_email='iglpdc@gmail.com',
		url='https://github.com/iglpdc/dmrg_helpers',
		license='MIT',
		classifiers=[
			'Enviroment :: Console',
			'Development Status :: 0 - Beta',
			'Intended Audience :: Developers',
			'Intended Audience :: Science/Research',
			'License :: OSI Approved :: MIT license',
			'Natural language :: English',
			'Programming Language:: Python',
			'Topic :: Scientific/Engineering',
			'Topic :: Scientific/Engineering :: Physics',
			],
        # list all subdirectories in next list
		packages = ['dmrg_helpers', 'NAME.core',
			    'dmrg_helpers.utils'],
		py_modules = ['version'],
		requires = [],
		)
