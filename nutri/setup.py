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

#from setuptools import setup
from distutils.core import setup

setup(
    name='nutri',
    packages=['libnutri'],
    # entry_points={
    #     'console_scripts': [
    #         'command-name = nutri:main',
    #     ],
    # },
    scripts=['nutri'],
    version='0.0.0dev0',
)
