#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:17:57 2018

@author: shane
NOTICE
    This file is part of nutri, a nutrient analysis program.
        https://github.com/gamesguru/nutri
        https://pypi.org/project/nutri/

    nutri is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
END NOTICE
"""

import subprocess
import shutil
import os


def cmd(cmds, self_debug=False):
    if self_debug:
        print(cmds)
    _output = subprocess.check_output(cmds, stderr=subprocess.STDOUT, shell=True, encoding='850')
    if self_debug:
        print(_output)
    return _output.splitlines()


def attached_serials():
    lst = []
    for line in cmd('adb devices'):
        if '\tdevice' in line:
            lst.append(line.split('\t')[0])
    return lst


def adb_listdir(dir):
    return cmd(f'adb shell ls "{dir}"')


def adb_cat(file):
    return cmd(f'adb shell cat "{file}"')


def adb_push(localfile, remotefile):
    cmd(f'adb push "{localfile}" "{remotefile}"')


def main():
    adbpath = shutil.which('adb')
    # Exit if adb not in path
    if adbpath is None:
        exit(f"error: `adb' not found in path, please refer to help docs")
    serials = attached_serials()
    # Exit if zero, or two or more devices attached
    if len(serials) != 1:
        exit(f'error: we have {len(serials)} android devices, need exactly 1')
    sync(serials[0])


nutridir = os.path.join(os.path.expanduser('~'), '.nutri')


def sync(serial):
    print(f'sync: {serial}')
    # TODO: verify db, currently overwrites desktop over mobile each sync
    adb_push(f'{nutridir}/db', '/storage/emulated/0/nutri/db')
    # adb_push(f'{nutridir}/field', '/storage/emulated/0/nutri/field')
    # adb_push(f'{nutridir}/user', '/storage/emulated/0/nutri/user')


if __name__ == '__main__':
    main()
