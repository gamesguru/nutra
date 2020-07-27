#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:13:45 2020

@author: shane
"""

import os

from .analyze import day_analyze, foods_analyze
from .search import search_results
from .usda import (
    list_nutrients,
    sort_foods_by_kcal_nutrient_id,
    sort_foods_by_nutrient_id,
)


def nutrients(args, unknown, arg_parser=None, **kwargs):
    return list_nutrients()


def search(args, unknown, arg_parser=None, subparsers=None):
    """ Searches all dbs, foods, recipes, recents and favorites. """
    if len(unknown) < 1:
        subparsers["search"].print_help()
    else:
        return search_results(words=unknown)


def sort(args, unknown, arg_parser=None, subparsers=None):
    nutr_id = args.nutr_id
    if not nutr_id:
        subparsers["sort"].print_help()
    elif unknown:
        print(f"error: {len(unknown)} unknown extra args: {unknown}")
    elif args.kcal:
        return sort_foods_by_kcal_nutrient_id(nutr_id)
    else:
        return sort_foods_by_nutrient_id(nutr_id)


def analyze(args, unknown, arg_parser=None, subparsers=None):
    food_id = args.food_id

    if not food_id:
        subparsers["anl"].print_help()
    elif unknown:
        print(f"error: {len(unknown)} unknown extra args: {unknown}")
    else:
        return foods_analyze(food_id)


def day(args, unknown, arg_parser=None, subparsers=None):

    day_csv_path = args.food_log
    if day_csv_path:
        day_csv_path = os.path.expanduser(day_csv_path)

    if not day_csv_path:
        subparsers["day"].print_help()
    elif len(unknown) == 0:
        return day_analyze(day_csv_path)
    elif len(unknown) == 1:
        rda_csv_path = os.path.expanduser(unknown[0])
        return day_analyze(day_csv_path, rda_csv_path=rda_csv_path)
    else:
        print(f"error: {len(unknown)} unknown extra args: {unknown}")
