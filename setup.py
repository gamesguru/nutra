# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 16:30:30 2018

@author: shane
"""

import os
import shutil
import sys

from setuptools import setup

# Old pip doesn't respect `python_requires'
if sys.version_info < (3, 6, 5):
    ver = ".".join([str(x) for x in sys.version_info[0:3]])
    print("ERROR: nutra requires Python 3.6.5 or later to install")
    print("HINT:  You're running Python " + ver)
    exit(1)

# cd to parent dir of setup.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))
shutil.rmtree("dist", True)

CLASSIFIERS = [
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Education",
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]

REQUIREMENTS = ["colorama", "tabulate", "requests", "python-dotenv"]

README = open("README.rst").read()

PKG_NAME = "nutra"

setup(
    name=PKG_NAME,
    author="gamesguru",
    author_email="mathmuncher11@gmail.com",
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    python_requires=">=3.6.5",
    packages=["ntclient", "ntclient/utils"],
    entry_points={"console_scripts": ["nutra=ntclient.__main__:main"]},
    description="Home and office nutrient tracking software",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/nutratech/cli",
    license="GPL v3",
    version="0.0.19.dev0",
)

# Clean up
shutil.rmtree(f"{PKG_NAME}.egg-info", True)
shutil.rmtree(f"__pycache__", True)
shutil.rmtree(f".pytest_cache", True)
try:
    os.remove("MANIFEST")
except:
    pass
