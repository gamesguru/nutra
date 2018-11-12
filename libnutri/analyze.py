#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 23:57:03 2018

@author: shane
"""

import sys
import inspect
from libnutri import db

version = '0.0.1'


def analyze(PK_No=None, grams=100):
    dbs = db.fdbs()
    for d in dbs:
        for e in d.dbentries:
            if e.pk_no == PK_No:
                print(f'Analyze: {e.foodname} ({grams}g)\n')

                # Prints basic fields

                # Prints relative fields
                max_rel_length = 0
                for r in d.rels:
                    for re in r.rel_entries:
                        if re.pk_no == PK_No:
                            if float(re.nutramt) == 0.0:
                                continue
                            max_rel_length = max_rel_length if max_rel_length > len(re.nutrname) else len(re.nutrname)
                            # print(f'{re.nutrname} @ {re.nutramt}')
                for r in d.rels:
                    for re in r.rel_entries:
                        if re.pk_no == PK_No:
                            reamt = round(float(re.nutramt) * grams / 100, 2)
                            if reamt == 0.0:
                                continue
                            pad_rel_name = re.nutrname + ' ' * (max_rel_length - len(re.nutrname))
                            print(f'{pad_rel_name}  {reamt} mg')


def main(args=None):
    if args == None:
        args = sys.argv

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
            print(f"error: unknown option `{arg}'.  See 'nutri anl --help'.")
            break


def altcmd(i, arg):
    for i in inspect.getmembers(cmdmthds):
        for i2 in inspect.getmembers(i[1]):
            if i2[0] == 'altargs' and arg in i2[1]:
                return i[1].mthd
    return None


class cmdmthds:
    """ Where we keep the `cmd()` methods && opt args """
    class dbno:
        def mthd(rarg):
            if len(rarg) != 1 and len(rarg) != 2:
                exit(f'error: must specify only one PK_No, optionally followed by an amount in grams')
            try:
                PK_No = int(rarg[0])
            except:
                exit('error: invalid integer number for PK_No')
            try:
                grams = int(rarg[1])
            except:
                print('warn: no grams provided, using 100g')
                grams = 100
            analyze(PK_No, grams)
        altargs = ['-n']

    class help:
        def mthd(rarg):
            print(usage)
        altargs = ['-h', '--help']


usage = f"""Analyze ingredients, foods, recipes, and days.
Version {version}

Usage: nutri anl <option> [<value>]

Options:
    dbno | -n  analyze an ingredient by PK_No (NDB_No)"""
