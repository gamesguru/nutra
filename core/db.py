#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 10:23:50 2018

@author: shane
"""

import os
import re
import sys
import shutil
import inspect
import ntpath
from colorama import Style, Fore, Back, init

version = '0.0.1'

work_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(work_dir)


class RAWTABLE:
    def __init__(self, file):
        print(f'{Back.RED}Processing:{Style.RESET_ALL} {file}')
        # TODO: exit if config.txt exists, or prompt to overwrite
        with open(file, 'r') as f:
            lst = f.readlines()
        self.dir = os.path.dirname(file)
        self.headers = lst[0].split('\t')
        self.pheaders = self.headers
        self.colspan = len(self.headers)
        self.rows = []
        print(f'Your data has {self.colspan} columns and {len(lst)} rows.')  # , or {colspan * len(lst)} cells.')
        for n, row in enumerate(lst):
            self.rows.append(row)
            curspan = len(row.split('\t'))
            if not curspan == self.colspan:
                print(f'Error: only {curspan} elements (expect {self.colspan}) in row #{n}\n\n{row}')
                return None
            print(f'Verified {Fore.CYAN}{n}/{len(lst)} rows!{Style.RESET_ALL}')
        maxlength = 0
        for i, h in enumerate(self.headers):
            self.headers[i] = h.replace(' ', '_').rstrip()
            maxlength = maxlength if maxlength >= len(self.headers[i]) else len(self.headers[i])
        for i, h in enumerate(self.headers):
            self.pheaders[i] = h + ' ' * (maxlength - len(h) + 1)
        with open(f'{self.dir}/config.txt', 'w+') as f:
            for h in self.pheaders:
                f.write(h + '=\n')
        print(f'\n   A config file has been generated @ {Back.YELLOW}{Fore.BLUE}{self.dir}/config.txt{Style.RESET_ALL}\n   Please assign nutrients and run this script with the "--test" switch to check progress.  Pass in the "--import" switch when ready to import.')


class TEST:
    def __init__(self, directory):
        print(f'{Back.RED}Testing:{Style.RESET_ALL} {directory}\n')
        self.dir = directory
        lst = []
        with open(f'{self.dir}/config.txt', 'r') as f:
            for l in f.readlines():
                lst.append(l.rstrip())
        b = 0
        u = 0
        c = 0
        for l in lst:
            f = l.split('=')[1]
            if f == '':
                print(f'{Back.MAGENTA}{Fore.YELLOW}Blank field:{Style.RESET_ALL} {l}')
                b += 1
            elif not f in known_fields:
                print(f'{Back.RED}Unknown field:{Style.RESET_ALL} {l}')
                u += 1
            else:
                if ('(' in l and ')' in l) or ('[' in l and ']' in l):
                    ls = re.split('\(|\)|\[|\]', l.split('=')[0])
                    print(f'{Back.GREEN}{Fore.BLACK}Configure:{Style.RESET_ALL} {ls[0]}', end='')
                    print(f'{Fore.RED}({ls[1]}){Style.RESET_ALL}', end='')
                    print(f'{ls[2]}= {f}')
                else:
                    print(f'{Back.GREEN}{Fore.BLACK}Configure:{Style.RESET_ALL} {f}={l.split("=")[0]}')
                c += 1
        print(f'\nYou have {c}/{len(lst)} configured, {u} unknown, and {b} blank fields.\nIf you are satisfied with that, run this script again with the "--import" switch.')


class STAGE:
    def __init__(self, configfile):
        self.basename = os.path.splitext(configfile)[0]
        print(f'{Back.RED}Importing:{Style.RESET_ALL} {configfile}..', end='')
        # TODO: warn or abort if directory exists already, offer to rename?
        os.makedirs(f'staging/{self.basename}', 0o775, True)
        shutil.copy(configfile, f'staging/{self.basename}/data.txt')
        print(' done!\n')


def Add():
    for d in os.listdir('staging'):
        if os.path.isfile(d) and not d.startswith('_'):
            for f in os.listdir(d):
                if f == 'data.txt':
                    RAWTABLE(f'{d}/t{f}')


def Test():
    for d in os.listdir():
        if os.path.isdir(d) and not d.startswith('_'):
            TEST(d)


def Stage():
    for d in os.listdir():
        if os.path.isfile(d) and d.endswith('.txt'):
            STAGE(d)


coredir = os.path.dirname(os.path.realpath(__file__))


def main(args=None):
    global coredir
    if os.sep == '\\':
        init()
    if args == None:
        args = sys.argv
    print(f'\n{Fore.CYAN}Welcome to the DB import tool!{Style.RESET_ALL}\n')
    for i, arg in enumerate(args):
        rarg = args[i:]
        # Ignore first argument, as that is filename
        if arg == __file__:
            if len(args) == 1:
                print(usage)
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
        else:
            print(f"error: unknown option `{arg}'.  See 'nutri db -h'.")
            break

def altcmd(i, arg):
    for i in inspect.getmembers(cmdmthds):
        for i2 in inspect.getmembers(i[1]):
            if i2[0] == 'altargs' and arg in i2[1]:
                return i[1].mthd
    return None
    

class cmdmthds:
    """ Where we keep the `cmd()` methods && opt args """

    class stage:
        def mthd(rarg):
            Stage()

    class test:
        def mthd(rarg):
            Test()

    class add:
        def mthd(rarg):
            Add()


known_fields = [
    "FoodName",
    "NDBNo",
    "OthPrimKey",
    "OthPrimKey2",
    "OthPrimKey3",
    "Serv",
    "Serv2",
    "Weight",
    "Weight2",
    "ALA",
    "EpaDha",
    "Cals",
    "CalsFat",
    "FatTot",
    "FatSat",
    "FatTrans",
    "FatMono",
    "FatPoly",
    "Cholest",
    "Na",
    "K",
    "Carbs",
    "Fiber",
    "FiberSol",
    "Sugar",
    "Protein",
    "VitA",
    "VitC",
    "Ca",
    "Fe",
    "VitD",
    "VitE",
    "VitK",
    "B1",
    "B2",
    "B3",
    "B5",
    "B6",
    "B7",
    "B9",
    "B12",
    "Mg",
    "Zn",
    "Se",
    "B",
    "I",
    "P",
    "Mn",
    "F",
    "Cu",
    "Cr",
    "Mo",
    "Choline",
    "Inositol",
    "Carnitine",
    "Lipoic acid",
    "Aminos"
]

usage = f"""Database management tool
Version {version}

usage:
    --process    extract headers/columns and prep data
    --test       check your work before importing
    --import     copy the config and data over from the lib to the resource directory
"""


if __name__ == "__main__":
    main()
