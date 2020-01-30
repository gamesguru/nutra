#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 08:39:42 2018

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
import datetime


class Nutrient:
    def __init__(self, field, friendlyname=None, rda=None, units=None):
        self.field = field
        self.friendlyname = field if friendlyname is None else friendlyname
        self.rda = rda
        self.units = units
        nutrients.append(self)


nutrients = []
Nutrient("Calories", 2000, "cals")
Nutrient("Thiamin", 0.9, "mg")


class Food:
    def __init__(
        self, db, key, name, Nutrients=None, per_units=None
    ):  # fields? recipes? no. no.no
        self.db = db
        self.key = key
        self.name = name
        self.Nutrients = [] if Nutrients is None else Nutrients
        self.per_units = [] if per_units is None else per_units


class Recipe:
    def __init__(self, name, foods=None):
        self.name = name
        self.foods = [] if foods is None else foods


class Meal:
    def __init__(self, name, time=None, foods=None, recipes=None):
        self.name = name
        self.time = datetime.datetime.now() if time is None else time
        self.foods = [] if foods is None else foods
        self.recipes = [] if recipes is None else recipes


class Day:
    def __init__(self, date, meals=None):
        self.date = date
        meals = [] if meals is None else meals


# def main():
#     pass


# if __name__ == '__main__':
#     main()
