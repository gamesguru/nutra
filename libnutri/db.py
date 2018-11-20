#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 10:23:50 2018

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
import re
import sys
import numpy as np
import shutil
import inspect
import ntpath
from colorama import Style, Fore, Back, init
import timeit

version = '0.0.1'
nutridir = os.path.join(os.path.expanduser("~"), '.nutri')
dbdir = os.path.join(nutridir, 'db')


def gen_dbs():
    lst = []
    for dir in os.listdir(dbdir):
        lst.append(db(f'{dbdir}/{dir}'))
    return lst


class db:
    def __init__(self, dir):
        # tables
        self.tables = []
        for file in os.listdir(dir):
            self.tables.append(table(f'{dir}/{file}'))
        # perform relational algebra
        pass


class table:
    def __init__(self, file):
        self.schemas = []
        lines = []
        print(file)
        with open(file, 'r', encoding='utf8') as f:
            for line in f:
                lines.append(line)
                # print(line.rstrip())
        self.schemas = schematize(lines)
        pass


class schema:
    def __init__(self, Header, Entries):
        self.header = Header
        self.entries = Entries


class dbentry:
    def __init__(self, Key_No, FoodName, Nutrients, Servings):
        self.key = Key_No
        self.foodname = FoodName
        self.nutrients = Nutrients
        self.servings = Servings


class nutrient:
    def __init__(self, Key_NutrNo, NutrName, NutrAmt, Units):
        self.nutrno = Key_NutrNo
        self.nutrname = NutrName
        self.nutramt = NutrAmt
        self.units = Units


class serving:
    def __init__(self, house_unit, house_qty, std_unit, std_qty):
        """ Converts between household and standard units, e.g. 0.25 sec spray = 1 g """
        self.hunit = house_unit  # cups, 1 sec spray, sprigs, 1 sausage, etc.
        self.hqty = house_qty
        self.sunit = std_unit  # either g or mL
        self.sqty = std_qty


def schematize(lines):
    schemas = []
    headers = lines[0].split('\t')
    splitrows = [l.split('\t') for l in lines[1:]]
    for i, h in enumerate(headers):
        rows = [r[i] for r in splitrows]
        schemas.append(schema(h, rows))
    return schemas

    ######
    # legacy code below
    ######


def abbrev_fdbs():
    """ Returns a list of dbs, **NAMES ONLY** """
    lst = []
    for s in os.listdir(dbdir):
        fpath = os.path.join(dbdir, s)
        if os.path.isdir(fpath) and not s.startswith('&') and not s.startswith('_'):
            lst.append(s)
    return lst


def abbrev_rdbs():
    """ Returns a list of relative dbs (standalone, not tack on) """
    lst = []
    for s in os.listdir(dbdir):
        fpath = os.path.join(dbdir, s)
        if os.path.isdir(fpath) and s.startswith('_'):
            lst.append(s)
    return lst


def fdbs():
    """ Returns a list of flatfile dbs, data, and config (headers, fields, etc) """
    lst = []
    for s in os.listdir(dbdir):
        fpath = os.path.join(dbdir, s)
        if os.path.isdir(fpath):
            if not s.startswith('&') and not s.startswith('_'):
                lst.append(fdb(s))
    return lst


class fdb:
    """ The "full" db class, not just dbname as above """

    def __init__(self, dbname):
        self.name = dbname
        self.data = []
        self.config = []
        fpath = os.path.join(dbdir, self.name)
        if not os.path.isdir(fpath):
            print(f'error: no such db {self.name}')
            return None

        # Reads in config.txt and data.txt
        with open(f'{fpath}/config.txt', 'r') as f:
            for line in f.readlines():
                self.config.append(line.rstrip())
        with open(f'{fpath}/data.txt', 'r') as f:
            for line in f.readlines():
                self.data.append(line.rstrip())

        # Creates the headers from the config
        self.headers = gen_headers(self.config)

        # Allots data-entries into numpy array
        self.fdb_entries = []  # gen_fdb_entries(self.data, self.headers)
        # self.data = np.array(self.data[1:])
        # self.dbentries = []
        # for d in self.data:
        #     arr = np.array(d.split('\t'))
        #     # Creates `dbentry': args=(pk_no, foodname, fields)
        #     self.dbentries.append(dbentry(arr[self.fi("PK_No")], arr[self.fi("FoodName")], arr))

        # Reads in relative tackons if they exist
        relroot = os.path.join(dbdir, f'&{self.name}')
        self.rels = []
        if os.path.isdir(relroot):
            for d in os.listdir(relroot):
                self.rels.append(frel(f'{relroot}/{d}'))

    def fi(self, basicfieldname):
        """ Field index """
        for f in self.fields:
            if f.basic_field_name == basicfieldname:
                return f.index
        return None

    def pksearch(self, PK_No):
        """ Search by PK_No """
        for d in self.dbentries:
            if d.pk_no == PK_No:
                return d
        return None


class fdb_entry:
    """ A food entry and all its data """

    def __init__(self, data, headers):
        self.ffields = None
        # TODO: this
        # def __init__(self, PK_No, FoodName, Fields=[]):
        #     self.pk_no = int(PK_No)  # Unique, even across dbs.  Program reads all dbs into one numpy array, mandates unique pk_nos
        #     self.foodname = FoodName
        #     self.fields = Fields
        #     self.matchstrength = 0

    def __str__(self):
        return f'{self.pk_no} {self.foodname}'


class ffield:
    """ Flat file field, plus its value, TODO: units/rda """

    def __init__(self, basicfieldname, value):
        self.basic_field_name = basicfieldname
        self.value = value


def gen_fdb_entries(data, headers):
    lst = []
    # TODO: this, later
    return lst


class header:
    """ A header, its column index, friendly name and basic_field_name, and its RDA if it exists """

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


def gen_headers(config):
    """ Pairs the fields with headers based on config, LEAVE BLANK ONES IN THERE!! """
    lst = []
    for i, s in enumerate(config):
        friendlyname = s.split('=')[0].rstrip()
        basic_field_name = s.split('=')[1]
        # TODO: parse units if available
        lst.append(header(i, friendlyname, basic_field_name))
    return lst


class frel:
    def __init__(self, fpath):
        """ Relative add-on db constructor """
        self.config = []
        self.data = []
        self.key = []

        # Reads in config.txt, key.txt and data.txt
        with open(f'{fpath}/config.txt', 'r') as f:
            for line in f.readlines():
                self.config.append(line.rstrip())
        with open(f'{fpath}/data.txt', 'r') as f:
            for line in f.readlines():
                self.data.append(line.rstrip())
        with open(f'{fpath}/key.txt', 'r') as f:
            for line in f.readlines():
                self.key.append(line.rstrip())

        # Creates the pairs for field <--> header
        self.fields = gen_fields(self.config)
        # Creates the pairs for PK_NutrNo <--> NutrName
        self.frel_keys = gen_frel_keys(self.key, self.config)
        # Creates the pairs for field <--> header ???
        self.frel_entries = gen_frel_entries(self.data, self.config, self.frel_keys)


class frel_key:
    def __init__(self, PK_NutrNo, NutrName):
        self.pk_nutrno = PK_NutrNo
        self.nutrname = NutrName


def gen_frel_keys(key, config):
    # Determine friendlyname (header) for PK_NutrNo and NutrName (e.g. Nutr_No and NutrDesc in USDA)
    for c in config:
        if c.split('=')[1] == 'PK_NutrNo':
            pk_nutrno = c.split('=')[0].rstrip()
        elif c.split('=')[1] == 'NutrName':
            nutrname = c.split('=')[0].rstrip()

    # Figure out column index
    for i, k in enumerate(key[0].split('\t')):
        if k == pk_nutrno:
            pkni = i
        elif k == nutrname:
            nni = i

    # Allot "frel keys"
    frel_keys = []
    for k in key[1:]:
        frel_keys.append(frel_key(k.split('\t')[pkni], k.split('\t')[nni]))
    return frel_keys


class frel_entry:
    def __init__(self, PK_No, NutrName, NutrAmt):
        self.pk_no = PK_No
        self.nutrname = NutrName
        self.nutramt = NutrAmt

    def __str__(self):
        return f'{self.pk_no}: {self.nutrname} @{self.nutramt}'


def gen_frel_entries(data, config, rel_keys):
    # Determine friendlyname (header) for PK_NutrNo and NutrName (e.g. Nutr_No and NutrDesc in USDA)
    for c in config:
        if c.split('=')[1] == 'PK_No':
            pk_no = c.split('=')[0].rstrip()
        elif c.split('=')[1] == 'PK_NutrNo':
            pk_nutrno = c.split('=')[0].rstrip()
        elif c.split('=')[1] == 'NutrAmt':
            nutramt = c.split('=')[0].rstrip()
    # Figure out column index
    for i, d in enumerate(data[0].split('\t')):
        if d == pk_no:
            pki = i
        elif d == pk_nutrno:
            pkni = i
        elif d == nutramt:
            namti = i
    # Allot rel entries
    frel_entries = []
    for d in data[1:]:
        pk_no = d.split('\t')[pki]
        pk_nutrno = d.split('\t')[pkni]
        nutrname = [n for n in rel_keys if n.pk_nutrno == pk_nutrno][0].nutrname
        nutramt = d.split('\t')[namti]
        frel_entries.append(frel_entry(int(pk_no), nutrname, nutramt))
    # for r in rel_entries:
    #     print(r)
    return frel_entries


def main(args=None):
    global nutridir
    if os.sep == '\\':
        init()
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
            for db in abbrev_fdbs():
                print(f'flat: {db}')
            for rdb in abbrev_rdbs():
                print(f'rel:  {rdb[1:]}')
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
