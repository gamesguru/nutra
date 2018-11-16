#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 20:28:06 2018

@author: shane
NOTICE
    This file is part of nutri, a nutrient analysis program.
        https://github.com/gamesguru/nutri
        https://pypi.org/project/nutri/

    nutri is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    nutri is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with nutri.  If not, see <https://www.gnu.org/licenses/>.
END NOTICE
"""

import re
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
    dbs = db.fdbs()
    while True:
        query = input('> ')
        exits = ['', 'q', 'c']
        if query in exits:
            break
        else:
            search(query.split(), dbs)


def search(words, dbs=None):
    """ Searches all dbs, foods, recipes, recents and favorites. """
    # Current terminal height
    bheight = shutil.get_terminal_size()[1] - 2
    if dbs == None:
        dbs = db.fdbs()
    # Count word matches
    for d in dbs:
        for e in d.fdb_entries:
            for word in words:
                w = word.upper()
                for fword in re.split(' |,|/', e.foodname):
                    f = fword.upper()
                    # Checks for our search words in the FoodName, also anti_vowel(our words) e.g. BRST, CKD, etc
                    if ((w in f) or (len(w) > 5 and anti_vowel(w) in f)):
                        e.matchstrength += 2 * len(w) if e.foodname.startswith(w) else len(w)  # ONIONS,SWT,RAW vs "nutri search onion raw"
                        break

        # Sort by the strongest match
        d.fdb_entries.sort(key=operator.attrgetter('matchstrength'))
        d.fdb_entries.reverse()
    bestmatch = d.fdb_entries[0].matchstrength
    # Print off as much space as terminal allots, TODO: override flag to print more or print all results?
    n = 0
    for d in dbs:
        for e in d.fdb_entries:
            perc = round(100 * e.matchstrength / bestmatch, 1)
            print(f'{perc}%: {e}')
            n += 1
            if n == bheight:
                return


def anti_vowel(c):
    vowels = ('A', 'E', 'I', 'O', 'U')
    return ''.join([l for l in c if l not in vowels])


if __name__ == '__main__':
    main()
