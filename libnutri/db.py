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
        if dir.startswith('_') or dir.startswith('&'):
            continue  # TODO
        print(dir)  # REMOVE IN PRODUCTION!!
        lst.append(db(f'{dbdir}/{dir}'))
    return lst


def bench(mthd=gen_dbs):
    print('Timeit: ' + str(timeit.timeit(mthd, number=1) * 1000) + ' ms')


rdas = []


class rda:
    def __init__(self, nute, rda, units):
        self.nute = nute
        self.rda = rda
        self.units = units


# Redis here
with open(f'{nutridir}/user/rda.txt', 'r', encoding='utf8') as f:
    for line in f:
        if line.startswith('#'):
            continue
        l = line.split('#')[0].strip()
        n = l.split('=')[0]
        r = float(l.split('=')[1].split()[0])
        try:
            u = l.split('=')[1].split()[1]
        except:
            u = str()
        # print(f'{n}: {r} {u}')
        rdas.append(rda(n, r, u))


# and here
class db:
    def __init__(self, dir):
        # tables
        self.dir = dir
        self.tables = []
        for file in os.listdir(dir):
            self.tables.append(table(f'{dir}/{file}'))
        self.entries = []

        # for t in self.tables:
        #     print(t.name)
        #     for h in t.headers:
        #         print('   ' + h)

        # gen_entries(self.tables)

        # self.entries = entries(self.tables)
        # for e in self.entries:
        #     print(e)

        for t in self.tables:
            if t.name.startswith('DATA_'):
                for l in t.lines:
                    Key_NutrNo = ''
                    Nutr_Val = ''
                    nute = nute_entry(Key_NutrNo, Nutr_Val)
                    self.append_entry(self, nute)

        self.nutrients = nutrients(self)
        pkis = set()

        # for t in self.tables:
        #     if t.name.startswith('DATA_'):
        #         for line in t.lines:
        #             els = line.split('\t')
        #             if els[t.pki] in pkis:
        #                 e = next((e for e in self.entries if e.pki == ), None)
        #             if any(e.key == key for e in self.entries):
        #                 pass
        #             else:
        #                 pass

        # schemas = [s for s in ]
        # for t1 in self.tables:
        #     print(t1.name)
        #     for t2 in self.tables:
        #         if t1 == t2:
        #             continue
        #         for s1 in t1.schemas:
        #             for s2 in t2.schemas:
        #                 if s1.header == s2.header:
        #                     # if t1.name.startswith('DATA_'):
        #                     #     continue
        #                     # if s1.iskey:
        #                     print(f'{s1.header}: {t1.name} <--> {t2.name}')
        print()

    def append_entry(self, Key_No, nute_entry):  # TODO: remove from line
        if any(e.key == Key_No for e in self.entries):
            e = next(e.key == Key_No for e in self.entries)
            print(type(e))
            e.add_nute(nute_entry)
        else:
            e = entry(Key_No)
            e.add_nute(nute_entry)
            self.entries.append(e)
        self.entries = set()

        for t in self.tables:
            if t.name.startswith('DATA_'):
                pki = -1
                nki = -1
                nvi = -1
                pki = t.headers.index('Key_No')
                nki = t.headers.index('Key_NutrNo')
                nvi = t.headers.index('Nutr_Val')

                for l in t.lines:
                    splits = l.split('\t')

                    Key_No = splits[pki]
                    Key_NutrNo = splits[nki]
                    Nutr_Val = splits[nvi]

                    nute = nute_entry(Key_NutrNo, Nutr_Val)
                    self.append_entry(Key_No, nute)

        self.nutrients = nutrients(self)
        # pkis = set()
        print()

    # def append_entry(self, Key_No, nute_entry):
    #     # if any(e.key == Key_No for e in self.entries):
    #     for e in self.entries:
    #         if e.key == Key_No:
    #             e.add_nute(nute_entry)
    #             # print(f'add: {e.key} --> {nute_entry.nutrno}')
    #             return

    #         # e = next(e.key == Key_No for e in self.entries)
    #         # print(type(e))
    #         # e.add_nute(nute_entry)
    #     # else:
    #     e = entry(Key_No)
    #     e.add_nute(nute_entry)
    #     self.entries.add(e)
    #     if len(self.entries) % 100 == 0:
    #         print(len(self.entries))
    #     # print(f'create: {e.key}')


class table:
    def __init__(self, file):
        self.name = os.path.splitext(ntpath.basename(file))[0]
        # self.schemas = []
        # print(file)
        self.lines = []
        with open(file, 'r', encoding='utf8') as f:
            for line in f:
                self.lines.append(line.rstrip())
        self.headers = self.lines[0].split('\t')
        # self.pki = self.headers.index('Key_No')
        # self.nki = self.headers.index('Key_NutrNo')
        # self.nvi = self.headers.index('Nutr_Val')

        # self.schemas = schematize(lines)


# class schema:
#     def __init__(self, Header, Entries):
#         self.header = Header
#         self.iskey = self.header.startswith('Key_')
#         self.entries = Entries

# class entries:


class entry:
    def __init__(self, Key_No):
        self.key = Key_No
        self.foodname = None
        self.nutrients = []  # nutrients

    def add_nute(self, nute_entry):
        self.nutrients.append(nute_entry)


def entries(tables):
    entries = []
    lines = []
    for t in tables:
        if t.name == 'DATA_MAIN':
            for l in t.lines:
                lines.append(l)
    headers = lines[0].split('\t')
    pki = -1
    nki = -1
    nvi = -1
    for i, h in enumerate(headers):
        if h == ', NutrAmt=0':
            pki = i
        elif (h == 'Key_NutrNo'):
            nki = i
        elif h == 'Nutr_Val':
            nvi = i
    for l in lines:
        entries.append(entry())
    return entries

    for t1 in tables:
        print(t1.name)
        for h in t1.headers:
            if h.startswith('Key_'):
                print('   ' + h)
        for t2 in tables:
            if t1 == t2:
                continue
    return entries


class nute_entry:
    def __init__(self, Key_NutrNo, Nutr_Val):
        self.nutrno = Key_NutrNo
        self.nutramt = Nutr_Val


class nutrient:
    def __init__(self, Key_NutrNo, NutrName, Units, NutrAmt=0):
        self.nutrno = Key_NutrNo
        self.nutrname = NutrName
        self.nutramt = NutrAmt
        self.units = Units


def nutrients(db):
    ret = []
    lines = []
    with open(f'{db.dir}/NUTR_DEF.txt', 'r') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
    headers = lines[0].split('\t')
    pki = -1
    uni = -1
    nni = -1
    for i, h in enumerate(headers):
        if (h == 'Key_NutrNo'):
            pki = i
        elif h == 'NutrUnit':
            uni = i
        elif h == 'NutrName':
            nni = i
    for l in lines[1:]:
        els = l.split('\t')
        ret.append(nutrient(els[pki], els[nni], els[uni]))
    return ret

# class rdbentry:
#     def __init__(self, Key_No):
#         self.key = Key_No
#         self.foodname = None
#         self.nutrients = None


# class rnutrient:
#     def __init__(self, Key_NutrNo, NutrName, NutrAmt, Units):
#         self.nutrno = Key_NutrNo
#         self.nutrname = NutrName
#         self.nutramt = NutrAmt
#         self.units = Units

# class serving:
#     def __init__(self, house_unit, house_qty, std_unit, std_qty):
#         """ Converts between household and standard units, e.g. 0.25 sec spray = 1 g """
#         self.hunit = house_unit  # cups, 1 sec spray, sprigs, 1 sausage, etc.
#         self.hqty = house_qty
#         self.sunit = std_unit  # either g or mL
#         self.sqty = std_qty

# def schematize(lines):
#     schemas = []
#     headers = lines[0].split('\t')
#     splitrows = [l.split('\t') for l in lines[1:]]
#     for i, h in enumerate(headers):
#         rows = [r[i] for r in splitrows]
#         schemas.append(schema(h.rstrip(), rows))
#     return schemas


#####################
# legacy code below #
#####################


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
        args = sys.argv[1:]

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

    class list:
        def mthd(rarg):
            for db in abbrev_fdbs():
                print(f'flat: {db}')
            for rdb in abbrev_rdbs():
                print(f'rel:  {rdb[1:]}')
        altargs = ['-l']

    class bench:
        """ REMOVE IN PRODUCTION!! """
        def mthd(rarg):
            bench()
        altargs = ['-b']

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

usage = f"""nutri: Database management tool
Version {version}

Usage: nutri db <command>

Commands:
    list | -l  list off databases stored on your computer"""

if __name__ == "__main__":
    main()
