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

long_description = 'Nothing to say here.'

#from setuptools import setup
from distutils.core import setup

setup(
    name='nutri',
    packages=['libnutri'],
    # packages=setuptools.find_packages(),
    author='gamesguru',
    author_email='bitcommander@zoho.com',
    description='Home and offic nutrient tracking software',
    # entry_points={
    #     'console_scripts': [
    #         'command-name = nutri:main',
    #     ],
    # },
    scripts=['nutri'],
    install_requires=['colorama'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.0dev1',
    url="https://github.com/gamesguru/nutri",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
