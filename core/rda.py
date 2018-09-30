#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 08:39:42 2018

@author: shane
"""

import os
import datetime


class Nutrient:
    def __init__(self, field, rda, units=None, friendlyname=field):
        self.friendlyname = friendlyname
        self.field = field
        self.rda = rda
        self.units = units
        nutrients.append(self)


nutrients = []
Nutrient('Calories', 2000, 'cals')
Nutrient('Thiamin', 0.9, 'mg')


class Food:
    def __init__(self, db, key, name, Nutrients=None, per_units=None):  # fields? recipes? no. no.no
        self.db = db
        self.key = key
        self.name = name
        self.Nutrients = [] if Nutrients is None else Nutrients
        self.per_units = [] if per_units is None else per_units


class Recipe:
    def __init__(self, name, foods=None):
        self.name = name
        self.foods = [] if foods is None else foods

# def main():
#     pass


# if __name__ == '__main__':
#     main()
