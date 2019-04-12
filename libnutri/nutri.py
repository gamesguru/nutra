#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 22:25:38 2018

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
import os
import inspect
from libnutri import remote, search, rank

# First thing's first, check Python version
if sys.version_info < (3, 6, 5):
    exit("ERROR: nutri requires Python 3.6.5 or later to run.")

version = '0.0.1'

usage = f"""nutri helps you stay fit and healthy.
Version {version}

Usage: nutri <command>

Commands:
    config                  change name, age, and vitamin targets
    search                  search database by food name
    analyze | anl           critique a date (range), meal, recipe, or food
    remote                  login, logout, register, and online functions
    --help | -h             show help for a given command"""


def main(args=None):
    """ Parses the args and hands off to submodules """
    if args == None:
        args = sys.argv
    # print(args)
    # No arguments passed in
    if len(args) == 0:
        print(usage)
    else:
        # Pop off arg0
        if args[0].endswith('nutri'):
            args.pop(0)
        if len(args) == 0:
            print(usage)

    # Otherwise we have some args
    # print(args)
    for i, arg in enumerate(args):
        rarg = args[i:]
        # Ignore first argument, as that is filename
        if arg == __file__:
            if len(args) == 1:
                print(usage)
                continue
            else:
                continue
        # Activate method for command, e.g. `help'
        elif hasattr(cmdmthds, arg):
            getattr(cmdmthds, arg).mthd(rarg[1:])
            break
        # Activate method for opt commands, e.g. `-h' or `--help'
        elif altcmd(i, arg) != None:
            altcmd(i, arg)(rarg[1:])
            break
        # Otherwise we don't know the arg
        print(f"nutri: `{arg}' is not a nutri command.  See 'nutri help'.")
        break


def altcmd(i, arg):
    for i in inspect.getmembers(cmdmthds):
        for i2 in inspect.getmembers(i[1]):
            if i2[0] == 'altargs' and arg in i2[1]:
                return i[1].mthd
    return None


class cmdmthds:
    """ Where we keep the `cmd()` methods && opt args """

    class config:
        def mthd(rarg):
            config.main(rarg)

    class search:
        altargs = ['-s']

        def mthd(rarg):
            search.main(rarg)

    class rank:
        altargs = ['-r']

        def mthd(rarg):
            rank.main(rarg)

    class analyze:
        altargs = ['anl']

        def mthd(rarg):
            analyze.main(rarg)

    class remote:
        def mthd(rarg):
            remote.main(rarg)

    class help:
        altargs = ['--help', '-h']

        def mthd(rarg):
            print(usage)


if __name__ == "__main__":
    main()
