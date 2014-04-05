#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='django-country-context',
    version='1.0.0',
    url='https://github.com/mpcabd/django-country-context',
    description='Country context for Django, to handle multiple countries sites',
    license='GPLv3+',
    long_description=open('README.md').read(),
    author='Abd Allah Diab',
    author_email='mpcabd@gmail.com',
    platforms=['any'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django'
    ],
    requires=['django'],
)