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

long_description = """An extensible nutrient tracking app designed for home and office use.  CLI backend.
Functions:
- Import databases, relative or extended.  Comes with the USDA data: 8000+ foods and 50+ nutrients.
- Define custom fields (ORAC, IF, GI).  Pair custom fields to main DBs by food name.
- Add custom databases, fields, recipes, foods and ingredients.
- Track individual targets and rate outcomes.
- Merge daily strategies and meals tracked on the PC with your mobile Android app com.github.nutri
- Colored and charted printouts, limit by date or nuitrient."""

#from setuptools import setup
from distutils.core import setup

setup(
    name='nutri',
    packages=['libnutri'],
    # packages=setuptools.find_packages(),
    author='gamesguru',
    author_email='mathmuncher11@gmail.com',
    description='Home and office nutrient tracking software',
    # entry_points={
    #     'console_scripts': [
    #         'command-name = nutri:main',
    #     ],
    # },
    scripts=['nutri'],
    install_requires=['colorama'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.0.dev3',
    url="https://github.com/gamesguru/nutri",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
