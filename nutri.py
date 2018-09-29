#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 22:25:38 2018

@author: shane
"""

import sys
from core import nutri_db

def exc_main():
    for i, arg in enumerate(sys.argv):
        if arg == __file__:
            continue
        elif arg == 'db':
            print(' '.join(sys.argv[i + 1:]))
            nutri_db.exc_main(' '.join(sys.argv[i:]))
            break

if __name__ == "__main__":
    exc_main()
