#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 22:25:38 2018

@author: shane
"""

import sys
from core import db, user

def exc_main():
    for i, arg in enumerate(sys.argv):
        larg = sys.argv[i + 1:]
        #sarg = ' '.join(larg)
        if arg == __file__:
            continue
        elif arg == 'db':
            db.exc_main(larg)
            break
        elif arg == 'user':
            user.exc_main(larg)

if __name__ == "__main__":
    exc_main()
