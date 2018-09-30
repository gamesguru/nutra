#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 22:25:38 2018

@author: shane
"""

import sys
from core import db, user


def main():
    if len(sys.argv) == 1:
        usage()
    else:
        arg = sys.argv[1]
        rarg = sys.argv[2:]
        if not arg in cmds:
            exit(f"nutri: error: '{arg}' is not a nutri command.  See 'nutri --help.\n")
        elif arg == 'db':
            db.main(rarg)
        elif arg == 'user':
            user.main(rarg)


cmds = ['db', 'user']


def usage():
    print(f"""Nutritracker helps you stay fit and healthy.
Version 0.0.1

Usage: {fmt.BOLD}nutri <command>{fmt.END}

Commands:
    {fmt.BOLD}user{fmt.END}                create, edit and switch users
    {fmt.BOLD}add{fmt.END}                 add foods or items to daily log
    {fmt.BOLD}search{fmt.END}              search databases or fields
    {fmt.BOLD}db{fmt.END}                  import, edit and verify databases
    {fmt.BOLD}fields{fmt.END}              import, pair and manage fields
    {fmt.BOLD}log{fmt.END}                 show previous meals and summary
    {fmt.BOLD}contrib{fmt.END}             rank contributions
    {fmt.BOLD}sync{fmt.END}                sync android device""")


class fmt:
    BOLD = '\033[1m'
    END = '\033[0m'


if __name__ == "__main__":
    main()
