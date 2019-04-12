#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 20:28:06 2018

@author: shane
NOTICE
    This file is part of nutri, a nutrient analysis program.
        https://github.com/gamesguru/nutri
        https://pypi.org/project/nutri/

    nutri is an extensible nutrient analysis and composition application.
    Copyright (C) 2018  Shane Jaroch

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
END NOTICE
"""

import sys
import shutil
import inspect
from libnutri import remote


def search(words, dbs=None):
    """ Searches all dbs, foods, recipes, recents and favorites. """
    # Current terminal height
    bufferheight = shutil.get_terminal_size()[1] - 2
    bufferwidth = shutil.get_terminal_size()[0]

    params = dict(
        terms=','.join(words)
    )

    response = remote.request('search', params=params)
    results = response.json()['data']['message']

    lfoodid = 0
    lfoodname = 0
    for r in results:
        food_id = str(r['food_id'])
        food_name = str(r['long_desc'])

        if len(food_id) > lfoodid:
            lfoodid = len(food_id)
        if len(food_name) > lfoodname:
            lfoodname = len(food_name)

    for i, r in enumerate(results):
        if i == bufferheight:
            break
        food_id = str(r['food_id'])
        food_name = str(r['long_desc'])
        avail_buffer = bufferwidth - len(food_id) - 12
        if len(food_name) > avail_buffer:
            print(f'{food_id.ljust(lfoodid)}    {food_name[:avail_buffer]}...')
        else:
            print(f'{food_id.ljust(lfoodid)}    {food_name}')


def rank(rargs):
    nutr_no = rargs[0]
    words = rargs[1:]
    bufferheight = shutil.get_terminal_size()[1] - 2
    bufferwidth = shutil.get_terminal_size()[0]

    params = dict(
        nutr_no=nutr_no,
        terms=','.join(words)
    )

    response = remote.request('sort', params=params)
    print(response)
    results = response.json()['data']['message']


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    words = []

    # No arguments passed in
    if len(args) == 0:
        print(usage)

    # Otherwise we have some args
    for i, arg in enumerate(args):
        rarg = args[i:]
        if hasattr(cmdmthds, arg):
            getattr(cmdmthds, arg).mthd(rarg[1:])
            if arg == 'help':
                break
        # Activate method for opt commands, e.g. `-h' or `--help'
        elif altcmd(i, arg) != None:
            altcmd(i, arg)(rarg[1:])
            if arg == '-h' or arg == '--help' or arg == '-r' or arg == '--rank':
                break
        # Otherwise we don't know the arg
        else:
            words.append(arg)

    if len(words) > 0:
        search(words)


def altcmd(i, arg):
    for i in inspect.getmembers(cmdmthds):
        for i2 in inspect.getmembers(i[1]):
            if i2[0] == 'altargs' and arg in i2[1]:
                return i[1].mthd
    return None


class cmdmthds:
    """ Where we keep the `cmd()` methods && opt args """

    class help:
        def mthd(rarg):
            print(usage)
        altargs = ['-h', '--help']

    class help:
        def mthd(rarg):
            rank(rarg)
        altargs = ['-r', '--rank']


usage = f"""nutri: Search tool

Usage: nutri search <flags> <query>

Flags:
    -u            search USDA only
    -b            search BFDB only
    -n            search nutri DB only
    -nub          search all three DBs
    --help | -h   print help"""

if __name__ == '__main__':
    main()
