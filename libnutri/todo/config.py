#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 23:44:06 2018

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

import os
import sys
import getpass
import inspect
from colorama import Style, Fore, Back, init


nutridir = f'{os.path.expanduser("~")}/.nutri'


def main(args=sys.argv):
    # os.chdir(os.path.expanduser("~"))
    # os.makedirs('.nutri/users', 0o755, True)

    if args == None:
        args = sys.argv

    # No arguments passed in
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
        print(f"error: unknown option `{arg}'.  See 'nutri config --help'.")
        break


def altcmd(i, arg):
    for i in inspect.getmembers(cmdmthds):
        for i2 in inspect.getmembers(i[1]):
            if i2[0] == 'altargs' and arg in i2[1]:
                return i[1].mthd
    return None


class cmdmthds:
    """ Where we keep the `cmd()` methods && opt args """

    class new:
        altargs = ['--new', '-n']

        def mthd(rarg):
            new_profile(rarg)

    class extra:
        altargs = ['-e']

        def mthd(rarg):
            if len(rarg) == 0:
                print(extras)
            elif len(rarg) == 2:
                econfig(rarg)
            else:
                print('error: must specify only one option, and one value')

    class help:
        altargs = ['--help', '-h']

        def mthd(rarg):
            print(usage)


def new_profile(rargs):
    """Creates a new profile, deletes old one."""
    name = getpass.getuser()
    gender = 'n'
    age = 0
    print('Warning: This will create a new profile (log and db are kept)\n')
    # Name
    inpt = input(f'Enter name (blank for {name}): ')
    if inpt != '':
        name = inpt
    # Gender
    while True:
        inpt = input(f'Gender? [m/f/n]: ')
        if inpt == 'm' or inpt == 'f' or inpt == 'n':
            gender = inpt
            break
    # Age
    while True:
        inpt = input(f'Age: ')
        try:
            inpt = int(inpt)
            if inpt > 0 and inpt < 130:
                age = inpt
                break
        except:
            pass
    # Write new profile
    os.makedirs(nutridir, 0o775, True)
    with open(f'{nutridir}/config.txt', 'w+') as f:
        f.write(f'Name:{name}\n')
        f.write(f'Gender:{gender}\n')
        f.write(f'Age:{age}\n')
    print("That's it for the basic config, you can see what more can be configured with `nutri config extras'")


def econfig(rarg):
    """ Configures extra settings: weight, height, wrist size, and nutrient targets """
    print(f'option: {rarg[0]}')
    print(f'value:  {rarg[1]}')
    print('error: feature not implemented yet')


""" Usage commands """
usage = f"""Usage: nutri config <option> [<value>]

Options:
    new          create a new profile (log and db are kept)
    extra | -e   list extra options, or configure a specific one
"""

""" Extras usage"""
extras = f"""Usage: nutri config -e <option> [<value>]

Options:
    ht         height
    wt         weight
    wrist      wrist size"""

if __name__ == "__main__":
    main()
