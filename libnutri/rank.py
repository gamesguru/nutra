#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 19:45:43 2019

@author: shane
NOTICE
    This file is part of nutri, a nutrient analysis program.
        https://github.com/gamesguru/nutri
        https://pypi.org/project/nutri/

    nutri is an extensible nutrient analysis and composition application.
    Copyright (C) 2019  Shane Jaroch

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
from tabulate import tabulate


def rank(type, rargs):
    words = rargs[1:]

    if type == 'nutr_no':
        nutr_no = int(rargs[0])
        params = dict(
            nutr_no=nutr_no
        )
        response = remote.request('sort', params=params)
        results = response.json()['data']['message']
    else:  # tagname
        tagname = rargs[0]
        params = dict(
            tagname=tagname
        )
        response = remote.request('sort', params=params)
        results = response.json()['data']['message']

    print_id_and_long_desc_and_nutr_val(results)


def print_id_and_long_desc_and_nutr_val(results):
    # Current terminal size
    bufferwidth = shutil.get_terminal_size()[0]
    bufferheight = shutil.get_terminal_size()[1]

    rows = []
    for i, r in enumerate(results[0]['foods']):
        if i == bufferheight - 4:
            break
        food_id = str(r['food_id'])
        food_name = str(r['long_desc'])
        nutr_val = str(r['nutr_val'])
        avail_buffer = bufferwidth - len(food_id) - len(nutr_val) - 25
        if len(food_name) > avail_buffer:
            rows.append([food_id, food_name[:avail_buffer] + '...', nutr_val])
        else:
            rows.append([food_id, food_name, nutr_val])
    print(tabulate(rows, headers=['food_id', 'food_name', 'nutr_val'], tablefmt='orgtbl'))


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    # No arguments passed in
    if len(args) == 0:
        print(usage)

    # Otherwise we have some args
    for i, arg in enumerate(args):
        rarg = args[i:]
        if hasattr(cmdmthds, arg):
            getattr(cmdmthds, arg).mthd(rarg[1:])
            break
        # Activate method for opt commands, e.g. `-h' or `--help'
        elif altcmd(i, arg) != None:
            altcmd(i, arg)(rarg[1:])
            break
        # Otherwise we don't know the arg
        else:
            print(f"error: unknown option `{arg}'.  See 'nutri rank --help'.")
            break


def altcmd(i, arg):
    for i in inspect.getmembers(cmdmthds):
        for i2 in inspect.getmembers(i[1]):
            if i2[0] == 'altargs' and arg in i2[1]:
                return i[1].mthd
    return None


class cmdmthds:
    """ Where we keep the `cmd()` methods && opt args """

    class nutrno:
        def mthd(rarg):
            rank('nutr_no', rarg)
        altargs = ['-n']

    class tagname:
        def mthd(rarg):
            rank('tagname', rarg)
        altargs = ['-t']

    class help:
        def mthd(rarg):
            print(usage)
        altargs = ['-h', '--help']


usage = f"""nutri: Rank foods by Nutr_No or Tagname

Usage: nutri search <flags> <query>

Flags:
    -n            search by Nutr_No
    -t            search by Tagname
    -u            filter USDA only
    -b            filter BFDB only
    -n            filter nutri DB only
    -nub          search all three DBs
    --help | -h   print help"""
