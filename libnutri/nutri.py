#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 22:25:38 2018

@author: shane
"""

import sys
import os
import inspect
from libnutri import db, rda, config

# First thing's first, check Python version
if sys.version_info < (3, 6, 5):
    exit("ERROR: nutri requires Python 3.6.5 or later to run.")


class fmt:
    if os.path.sep == '/':
        BOLD = '\033[1m'
        END = '\033[0m'
    else:
        BOLD = ''
        END = ''


version = '0.0.1'

usage = f"""Nutritracker helps you stay fit and healthy.
Version {version}


Usage: {fmt.BOLD}nutri <command> {fmt.END}

Commands:
    {fmt.BOLD}config{fmt.END}              change name, age, and vitamin targets
    {fmt.BOLD}db{fmt.END}                  import, edit and verify databases
    {fmt.BOLD}field{fmt.END}               import, pair and manage fields
    {fmt.BOLD}recipe{fmt.END}              create, edit and view foods and recipes
    {fmt.BOLD}search{fmt.END}              search databases or recipes
    {fmt.BOLD}add{fmt.END}                 add foods or items to daily log
    {fmt.BOLD}log{fmt.END}                 show previous meals and summary
    {fmt.BOLD}sync{fmt.END}                sync android device
    {fmt.BOLD}contrib{fmt.END}             rank contributions
    {fmt.BOLD}bugreport{fmt.END}           e-wires source code and your pesonal info"""


def main(args=None):
    """ Parses the args and hands off to submodules """
    if args == None:
        args = sys.argv
    print(args)
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
            getattr(cmdmthds, arg).mthd(rarg)
            break
        # Activate method for opt commands, e.g. `-h' or `--help'
        elif altcmd(i, arg) != None:
            altcmd(i, arg)(rarg)
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

    class db:
        def mthd(rarg):
            db.main(rarg)

    # TODO: bugreport
    # class bugreport:
    #     def mthd(rarg):
    #         bugreport.main(rarg)

    class help:
        altargs = ['--help', '-h']

        def mthd(rarg):
            print(usage)


if __name__ == "__main__":
    main()
