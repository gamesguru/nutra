# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 20:28:06 2018

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutraent analysis and composition application.
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
"""

import sys
import shutil
import inspect
from libnutra import remote
from tabulate import tabulate


def cmd_search(args, unknown, arg_parser=None):
    return search(words=unknown)


def print_id_and_long_desc(results):
    # Current terminal size
    bufferwidth = shutil.get_terminal_size()[0]
    bufferheight = shutil.get_terminal_size()[1]

    rows = []
    for i, r in enumerate(results):
        if i == bufferheight - 4:
            break
        food_id = str(r["food_id"])
        food_name = str(r["long_desc"])
        avail_buffer = bufferwidth - len(food_id) - 15
        if len(food_name) > avail_buffer:
            rows.append([food_id, food_name[:avail_buffer] + "..."])
        else:
            rows.append([food_id, food_name])
    print(tabulate(rows, headers=["food_id", "food_name"], tablefmt="orgtbl"))


def search(words, dbs=None):
    """ Searches all dbs, foods, recipes, recents and favorites. """
    params = dict(terms=",".join(words))

    response = remote.request("search", params=params)
    results = response.json()["data"]

    print_id_and_long_desc(results)


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
            if arg == "help":
                break
        # Activate method for opt commands, e.g. `-h' or `--help'
        elif altcmd(i, arg) != None:
            altcmd(i, arg)(rarg[1:])
            if arg == "-h" or arg == "--help":
                break
        # Otherwise we don't know the arg
        else:
            words.append(arg)

    if len(words) > 0:
        search(words)


def altcmd(i, arg):
    for i in inspect.getmembers(cmdmthds):
        for i2 in inspect.getmembers(i[1]):
            if i2[0] == "altargs" and arg in i2[1]:
                return i[1].mthd
    return None


class cmdmthds:
    """ Where we keep the `cmd()` methods && opt args """

    class help:
        def mthd(rarg):
            print(usage)

        altargs = ["-h", "--help"]

    class rank:
        def mthd(rarg):
            rank(rarg)

        altargs = ["-r", "--rank"]


usage = f"""nutra: Search tool

Usage: nutra search <flags> <query>

Flags:
    -r            rank foods by Nutr_No or Tagname
    -u            search USDA only
    -b            search BFDB only
    -n            search nutra DB only
    -nub          search all three DBs
    --help | -h   print help"""

if __name__ == "__main__":
    main()
