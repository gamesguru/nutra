#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 20:28:06 2018

@author: shane
"""

import os
import sys
import shutil
import operator
from libnutri import db


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
            for word in words:
                f = e.foodname
                w = word.upper()
                # Checks for our search words in the FoodName, also anti_vowel(our words) e.g. BRST, CKD, etc
                if ((w in f) or (len(w) > 4 and anti_vowel(w) in f)):  # and not (w == 'CHICKEN'):
                    e.matchstrength += len(w)

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


def anti_vowel(c):
    vowels = ('A', 'E', 'I', 'O', 'U')
    return ''.join([l for l in c if l not in vowels])


if __name__ == '__main__':
    main()
