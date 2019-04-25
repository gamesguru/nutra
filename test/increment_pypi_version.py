#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 23:06:01 2019

@author: shane
"""

import os
import requests

def version():
    url = "https://pypi.python.org/pypi/nutri/json"
    data = requests.get(url).json()
    version = data['info']['version']
    return version

old_version = version()
print(f'Current version: {old_version}')
new_version = input('New version: ')

if not new_version == '':
    print('not blank')

split_version = old_version.split('.')
if split_version[-1].startswith('dev'):
    split_version[-1] = 'dev' + str(int(split_version[-1].replace('dev', '')) + 1)
else:
    split_version[-1] = str(int(split_version[-1]) + 1)
new_version = '.'.join(split_version)

sed_cmd = f"sed -i 's/{old_version}/{new_version}/g' setup.py"
print(sed_cmd)
os.system(sed_cmd)
