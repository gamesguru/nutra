#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 16:30:30 2018

@author: shane
"""

import sys

print ('Checking Python version info...')
if sys.version_info < (3, 6, 5):
    exit("ERROR: nutri requires Python 3.6.5 or later to run.")


def readme():
    with open('README.rst') as f:
        return f.read()


from distutils.core import setup

setup(
    name='nutri',
    packages=['libnutri'],
    # packages=setuptools.find_packages(),
    author='gamesguru',
    author_email='mathmuncher11@gmail.com',
    description='Home and office nutrient tracking software',
    entry_points={
        'console_scripts': [
            'nutri=libnutri.nutri:main',
        ],
    },
    # scripts=['nutri'],
    install_requires=['colorama'],
    long_description=readme(),
    long_description_content_type='text/x-rst',
    version='0.0.0.dev11',
    license='Apache v2',
    url="https://github.com/gamesguru/nutri",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)