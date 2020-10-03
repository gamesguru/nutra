#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:13:45 2020

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutrient analysis and composition application.
Copyright (C) 2018-2020  Shane Jaroch

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
"""

import os

from .analyze import day_analyze, foods_analyze
from .recipe import (
    recipe_add as _recipe_add,
    recipe_edit as _recipe_edit,
    recipe_overview,
    recipes_overview,
)
from .search import search_results
from .services.biometrics import biometric_add as _biometric_add
from .usda import (
    list_nutrients,
    sort_foods_by_kcal_nutrient_id,
    sort_foods_by_nutrient_id,
)


def nutrients(args, arg_parser=None, **kwargs):
    return list_nutrients()


def search(args, arg_parser=None, subparsers=None):
    """ Searches all dbs, foods, recipes, recents and favorites. """
    if args.terms:
        return search_results(words=args.terms)
    else:
        subparsers["search"].print_help()


def sort(args, arg_parser=None, subparsers=None):
    nutr_id = args.nutr_id
    if not nutr_id:
        subparsers["sort"].print_help()
    elif args.kcal:
        return sort_foods_by_kcal_nutrient_id(nutr_id)
    else:
        return sort_foods_by_nutrient_id(nutr_id)


def analyze(args, arg_parser=None, subparsers=None):
    food_ids = args.food_id
    grams = args.grams

    if not food_ids:
        subparsers["anl"].print_help()
    else:
        return foods_analyze(food_ids, grams)


def biometrics(args, arg_parser=None, subparsers=None):
    print("not implemented ;]")


def biometric_add(args, arg_parser=None, subparsers=None):
    bio_vals = {
        int(x.split(",")[0]): float(x.split(",")[1]) for x in args.biometric_val
    }

    return _biometric_add(bio_vals)


def recipe(args, arg_parser=None, subparsers=None):
    if args.recipe_id:
        return recipe_overview(args.recipe_id)
    else:
        return recipes_overview()


def recipe_add(args, arg_parser=None, subparsers=None):
    food_amts = {int(x.split(",")[0]): float(x.split(",")[1]) for x in args.food_amt}
    return _recipe_add(args.name, food_amts)


def recipe_edit(args, arg_parser=None, subparsers=None):
    return _recipe_edit(args.recipe_id)


def day(args, arg_parser=None, subparsers=None):
    day_csv_paths = args.food_log
    day_csv_paths = [os.path.expanduser(x) for x in day_csv_paths]
    if args.rda:
        rda_csv_path = os.path.expanduser(args.rda)

    if not day_csv_paths:
        subparsers["day"].print_help()
    elif not args.rda:
        return day_analyze(day_csv_paths)
    else:
        return day_analyze(day_csv_paths, rda_csv_path=rda_csv_path)


def sync(args, arg_parser=None, subparsers=None):
    from .sync import sync as _sync

    _sync()


def sync_register(args, arg_parser=None, subparsers=None):
    from getpass import getpass
    from .sync import register

    print("not implemented ;]")
    return

    email = input("email: ")
    confirm_email = input("confirm email: ")
    password = getpass("password: ")
    confirm_password = getpass("confirm password: ")

    if email != confirm_email or password != confirm_password:
        print("Try again, email and password must match")
        return

    register(email, password)


def sync_login(args, arg_parser=None, subparsers=None):
    from getpass import getpass
    from .sync import login

    password = getpass("password: ")
    login(args.email, password)
