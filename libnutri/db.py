#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 10:23:50 2018

@author: shane
"""

import os
import re
import sys
import numpy as np
import shutil
import inspect
import ntpath
from colorama import Style, Fore, Back, init

version = '0.0.1'


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
            elif not f in known_basic_fields:
                print(f'{Back.RED}Unknown field:{Style.RESET_ALL} {l}')
                u += 1
            else:
                if ('(' in l and ')' in l) or ('[' in l and ']' in l):
                    ls = re.split('\(|\)|\[|\]', l.split('=')[0])
                    print(f'{Back.GREEN}{Fore.BLACK}Configure:{Style.RESET_ALL}   {ls[0]}', end='')
                    print(f'{Fore.RED}({ls[1]}){Style.RESET_ALL}', end='')
                    print(f'{ls[2]}= {f}')
                else:
                    print(f'{Back.GREEN}{Fore.BLACK}Configure:{Style.RESET_ALL}   {l.split("=")[0]}= {f}')
                c += 1
        print(f'\nYou have {c}/{len(lst)} configured, {u} unknown, and {b} blank fields.\nIf you are satisfied with that, run this script again with the "nutri db save" command.')


class PREP:
    def __init__(self, file):
        # stage
        self.basename = os.path.splitext(file)[0]
        if self.basename in dbs():
            print(f'error: db already exists, delete with: nutri db -d {self.basename}')
            return
        if os.path.isdir(f'nutri_staging/{self.basename}'):
            print(f'error: staged db already exists, please manually remove: nutri_staging/{self.basename}')
            return
        if len(os.listdir('nutri_staging')) > 0:
            print(f'error: one or more dbs already staged, please remove or test:')
            for o in os.listdir('nutri_staging'):
                print(f'\t{o}')
            return
        print(f'{Back.RED}Importing:{Style.RESET_ALL} {file}..', end='')
        os.makedirs(f'nutri_staging/{self.basename}', 0o775, True)
        shutil.copy(file, f'nutri_staging/{self.basename}/data.txt')
        print(' done!\n')

        # import
        print(f'{Back.RED}Processing:{Style.RESET_ALL} {file}')
        # TODO: exit if config.txt exists, or prompt to overwrite
        with open(file, 'r') as f:
            lst = f.readlines()
        self.dir = f'nutri_staging/{self.basename}'
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
            print(f'\rVerified {Fore.CYAN}{n + 1}/{len(lst)} rows!{Style.RESET_ALL}', end='')
        maxlength = 0
        for i, h in enumerate(self.headers):
            self.headers[i] = h.replace(' ', '_').rstrip()
            maxlength = maxlength if maxlength >= len(self.headers[i]) else len(self.headers[i])
        for i, h in enumerate(self.headers):
            self.pheaders[i] = h + ' ' * (maxlength - len(h) + 1)
        with open(f'{self.dir}/config.txt', 'w+') as f:
            for h in self.pheaders:
                f.write(h + '=\n')
        print(f'\n   A config file has been generated @ {Back.YELLOW}{Fore.BLUE}{self.dir}/config.txt{Style.RESET_ALL}\n   Please assign nutrients and run this script with the "--test" switch to check progress.  Pass in the "nutri db save" command when ready to import.')


def Prep():
    n = 0
    file = None
    for f in os.listdir():
        if os.path.isfile(f) and f.endswith('.txt'):
            n += 1
            file = f
    if n == 1:
        PREP(file)
    else:
        print('error: must have exactly one *.txt file in current working directory to prep data')


def Test():
    for d in os.listdir('nutri_staging'):
        dir = f'nutri_staging/{d}'
        if os.path.isdir(dir) and not d.startswith('_'):
            TEST(dir)


def Save():
    for d in os.listdir('nutri_staging'):
        dir = f'nutri_staging/{d}'
        if os.path.isdir(dir) and not d.startswith('_'):
            for f in os.listdir(dir):
                if f == 'data.txt':
                    shutil.move(dir, dbdir)
    # TODO: is this okay?  upload config.txt to bb for convenience
    # shutil.rmtree('nutri_staging')


nutridir = os.path.join(os.path.expanduser("~"), '.nutri')
dbdir = os.path.join(nutridir, 'db')
# TODO: better placement
# if not os.path.isdir(dbdir):
#     os.makedirs(dbdir, 0o775, True)


def dbs():
    """ Returns a list of dbs, names only """
    lst = []
    for s in os.listdir(dbdir):
        fpath = os.path.join(dbdir, s)
        if os.path.isdir(fpath):
            lst.append(s)
    return lst


def fdbs():
    """ Returns a list of dbs, data, and config (headers, fields, etc) """
    lst = []
    for s in os.listdir(dbdir):
        fpath = os.path.join(dbdir, s)
        if os.path.isdir(fpath):
            #print(fpath)
            lst.append(fdb(fpath))
    return lst


class fdb:
    def __init__(self, dbname):
        self.name = dbname
        self.data = []
        self.config = []
        fpath = os.path.join(dbdir, self.name)
        if not os.path.isdir(fpath):
            print(f'error: no such db {self.name}')
            return None
        with open(f'{fpath}/config.txt', 'r') as f:
            for line in f.readlines():
                self.config.append(line.rstrip())
        with open(f'{fpath}/data.txt', 'r') as f:
            for line in f.readlines():
                self.data.append(line.rstrip())
        # Creates the fields from the config
        self.fields = gen_fields(self.config)
        self.headers = self.data[0].split('\t')
        # Allots data into numpy array
        self.data = np.array(self.data[1:])
        self.dbentries = []
        for d in self.data:            
            arr = np.array(d.split('\t'))
            # Creates `dbentry': args=(pk_no, foodname, fields)
            self.dbentries.append(dbentry(arr[self.fi("PK_No")], arr[self.fi("FoodName")], arr))
        #self.dbentries = np.array(self.dbentries)
        #print(self.pksearch('01001'))
    
    def fi(self, basicfieldname): # field index
        for f in self.fields:
            if f.basic_field_name == basicfieldname:
                return f.index
        return None
    
    def pksearch(self, PK_No): # Search by PK_No
        for d in self.dbentries:
            if d.pk_no == PK_No:
                return d
        return None


class dbentry:
    """ A food entry and all its data """

    def __init__(self, PK_No, FoodName, Fields=[]):
        self.pk_no = PK_No  # Unique, even across dbs.  Program reads all dbs into one numpy array, mandates unique pk_nos
        self.foodname = FoodName
        self.fields = Fields
        self.matchstrength = 0
    
    def __str__(self):
        return f'{self.pk_no} {self.foodname}'


class field:
    """ A field, its column index, friendly name and basic_field_name, and its RDA if it exists """

    def __init__(self, index, friendlyname, basicfieldname, r=None):
        self.index = index
        self.friendlyname = friendlyname
        self.basic_field_name = basicfieldname
        self.rda = r
        

    def __str__(self):
        if self.rda is None:
            return f'{self.friendlyname}={self.basic_field_name}'
        else:
            return f'{self.friendlyname}={self.basic_field_name} ({self.rda})'


def gen_fields(config):
    lst = []
    for i, s in enumerate(config):
        friendlyname = s.split('=')[0].rstrip()
        basic_field_name = s.split('=')[1]
        # TODO: parse units if available
        lst.append(field(i, friendlyname, basic_field_name))
    return lst


def main(args=None):
    global nutridir
    if os.sep == '\\':
        init()
    if args == None:
        args = sys.argv

    # print(args)
    # No arguments passed in
    if len(args) == 0:
        print(usage)

    # Otherwise we have some args
    # print(args)
    # print(f'\n{Fore.CYAN}Welcome to the DB import tool!{Style.RESET_ALL}\n')
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
            print(f"error: unknown option `{arg}'.  See 'nutri db --help'.")
            break


def altcmd(i, arg):
    for i in inspect.getmembers(cmdmthds):
        for i2 in inspect.getmembers(i[1]):
            if i2[0] == 'altargs' and arg in i2[1]:
                return i[1].mthd
    return None


class cmdmthds:
    """ Where we keep the `cmd()` methods && opt args """

    class prep:
        def mthd(rarg):
            Prep()

    class test:
        def mthd(rarg):
            Test()

    class save:
        def mthd(rarg):
            Save()

    class delete:
        def mthd(rarg):
            if len(rarg) != 1:
                print('error: not exactly one db name specified to delete')
                return
            else:
                chosendb = os.path.join(dbdir, rarg[0])
                if os.path.isdir(chosendb):
                    print(f'deleting {rarg[0]}...')
                    shutil.rmtree(chosendb)
                else:
                    print(f'error: no such db {rarg[0]}')
        altargs = ['-d']

    class list:
        def mthd(rarg):
            for db in dbs():
                print(db)
        altargs = ['-l']

    class help:
        def mthd(rarg):
            print(usage)
        altargs = ['-h', '--help']


known_basic_fields = [
    "FoodName",
    "PK_No",  # The primary key (typically `NDBNo') it must be unique even across different dbs
    "Cals",
    "CalsFat",
    "FatTot",
    "FatSat",
    "FatTrans",
    "FatMono",
    "FatPoly",
    "Carbs",
    "Fiber",
    "FiberSol",
    "Sugar",
    "Protein",
    "Cholest",
    "Na",
    "K",
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
    "ALA",
    "EpaDha",
    "Lycopene",
    "LutZea",
    "Choline",
    "Inositol",
    "Carnitine",
    "Lipoic_acid",
    "Serv",
    "Serv2",
    "Weight",
    "Weight2",
]

usage = f"""Database management tool
Version {version}

Put text file into current working directory with no other text files.

Usage: nutri db <command>

Commands:
    prep       extract headers/columns, prep for manual config
    test       check your config.txt before importing
    save       import the db (config and data) to your profile
    list | -l  list off databases stored on your computer
    -d         delete a database by name"""


if __name__ == "__main__":
    main()
