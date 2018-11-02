#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 23:44:06 2018

@author: shane
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
        return
    else:
        # Pop off arg0
        if args[0].endswith('config'):
            args.pop(0)
        if len(args) == 0:
            print(usage)
            return

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
            getattr(cmdmthds, arg).mthd(rarg)
            break
        # Activate method for opt commands, e.g. `-h' or `--help'
        else:
            for i in inspect.getmembers(cmdmthds):
                for i2 in inspect.getmembers(i[1]):
                    if i2[0] == 'altargs' and arg in i2[1]:
                        i[1].mthd(rarg)
                        return
        # Otherwise we don't know the arg
        print(f"error: unknown option `{arg}'.  See 'nutri config --help'.")
        break


class cmdmthds:
    """ Where we keep the `cmd()` methods && opt args """

    class new:
        altargs = ['--new', '-n']

        def mthd(rarg):
            new_profile(rarg)

    class extras:
        def mthd(rarg):
            print(extras)

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


usage = f"""Usage: nutri config <option> [<value>]

Options:
    new        create a new profile (log and db are kept)
    -e         configure an extra option
    extras     help for extra options (height, weight, wrist size)
"""

extras = f"""Usage: nutri config -e <option> [<value>]

Options:
    ht         height
    wt         weight
    wrist      wrist size"""

if __name__ == "__main__":
    main()
