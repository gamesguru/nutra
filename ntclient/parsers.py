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
    elif unknown:
        print(f"error: {len(unknown)} unknown extra args: {unknown}")
    elif args.kcal:
        return sort_foods_by_kcal_nutrient_id(nutr_id)
    else:
        return sort_foods_by_nutrient_id(nutr_id)


def analyze(args, arg_parser=None, subparsers=None):
    food_id = args.food_id

    if not food_id:
        subparsers["anl"].print_help()
    elif unknown:
        print(f"error: {len(unknown)} unknown extra args: {unknown}")
    else:
        return foods_analyze(food_id)


def day(args, arg_parser=None, subparsers=None):
    day_csv_paths = args.food_log
    day_csv_paths = [os.path.expanduser(x) for x in day_csv_paths]
    rda_csv_path = os.path.expanduser(args.rda)

    if not day_csv_paths:
        subparsers["day"].print_help()
    elif not rda_csv_path:
        return day_analyze(day_csv_paths)
    else:
        return day_analyze(day_csv_paths, rda_csv_path=rda_csv_path)
