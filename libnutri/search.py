#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 20:28:06 2018

@author: shane
"""

import os
import sys
import re
import shutil
import operator
from libnutri import db
from difflib import SequenceMatcher


def main(args=sys.argv):
    if args == None:
        args = sys.argv

    # Launch interactive shell
    if len(args) == 0:
        shell()
    # Perform search and drop
    else:
        search(args)


def shell():
    """ Provides interactive shell with broadly similar function to `search()' """
    print("Welcome to the search shell! Enter nothing, `q', or `c' to quit")
    while True:
        query = input('> ')
        exits = ['', 'q', 'c']
        if query in exits:
            break
        else:
            search(query.split())


def search(words):
    """ Searches all dbs, foods, recipes, recents and favorites. """
    # Current terminal height
    bheight = shutil.get_terminal_size()[1] - 2
    # Count word matches
    dbs = db.fdbs()
    for d in dbs:
        for e in d.dbentries:
            for rword in re.split(' |,|/|;', e.foodname.upper()):
                for word in words:
                    w = word.upper()
                    f = e.foodname.upper()
                    # Checks for our search words in the FoodName, also anti_vowel(our words) e.g. BRST, CKD, etc
                    if (w in f) or (len(w) > 4 and anti_vowel(w) in f):
                        e.matchstrength += len(word)
        # Sort by the strongest match
        d.dbentries.sort(key=operator.attrgetter('matchstrength'))
        d.dbentries.reverse()
    # Print off as much space as terminal allots, TODO: override flag to print more or print all results?
    n = 0
    for d in dbs:
        for e in d.dbentries:
            print(f'{e.matchstrength}: {e}')
            n += 1
            if n == bheight:
                return

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def anti_vowel(c):
    vowels = ('A', 'E', 'I', 'O', 'U')
    return ''.join([l for l in c if l not in vowels])

def search2(args):
    """ Searches all dbs, foods, recipes, and favorites. """
    # Current terminal height
    bheight = shutil.get_terminal_size()[1] - 2
    # The main hustle
    dbdir = os.path.join(os.path.expanduser('~'), '.nutri', 'db')
    for d in db.dbs():
        data = []
        config = []
        with open(f'{dbdir}/{d}/data.txt', 'r') as f:
            data = f.readlines()
        with open(f'{dbdir}/{d}/config.txt', 'r') as f:
            config = f.readlines()
        # TODO: make below int reusable API, put in db module
        fn = None
        pk_no = None
        for line in config:
            line = line.rstrip()
            if line.split('=')[1] == 'FoodName':
                fn = line.split('=')[0].split()[0]
            elif line.split('=')[1] == 'PK_No':
                pk_no = line.split('=')[0].split()[0]
        # Grab & split headers
        headers = data[0]
        for i, h in enumerate(headers.split('\t')):
            foodname = None
            pk_no = None
            # header == Headers['FoodName'], e.g. Shrt_Desc
            for line in data:
                if h == fn:
                    # print(h)
                    foodname = line.rstrip().split('\t')[i]
                    print(foodname)
                # elif h == pk_no:
                #     pk_no = line.rstrip().split('\t')[i]
                # print(f'{pk_no}\t{foodname}')


if __name__ == '__main__':
    main()
