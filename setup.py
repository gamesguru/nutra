# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 16:30:30 2018

@author: shane
"""

import sys

print("Checking Python version info...")
if sys.version_info < (3, 6, 5):
    exit("ERROR: nutra requires Python 3.6.5 or later to run.")


def readme():
    with open("README.rst") as f:
        return f.read()


from distutils.core import setup

setup(
    name="nutra",
    packages=["libnutra"],
    author="gamesguru",
    author_email="mathmuncher11@gmail.com",
    description="Home and office nutrient tracking software",
    entry_points={"console_scripts": ["nutra=libnutra.nutra:main",],},
    install_requires=["colorama", "tabulate", "requests"],
    long_description=readme(),
    long_description_content_type="text/x-rst",
    version="0.0.0.dev23",
    license="GPL v3",
    url="https://github.com/gamesguru/nutra",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
