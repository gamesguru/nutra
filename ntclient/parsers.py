#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:13:45 2020

@author: shane
"""

import os

from .usda import (
    day_analyze,
    list_nutrients,
    sort_foods_by_kcal_nutrient_id,
    sort_foods_by_nutrient_id,
)


def nutrients(args, unknown, arg_parser=None, **kwargs):
    return list_nutrients()


def search():
    pass


def sort(args, unknown, arg_parser=None, subparsers=None):
    nutr_id = args.nutr_id
    if not nutr_id:
        subparsers["sort"].print_help()
    elif unknown:
        print(f"error: unknown extra args: {unknown}")
    elif args.kcal:
        return sort_foods_by_kcal_nutrient_id(nutr_id)
    else:
        return sort_foods_by_nutrient_id(nutr_id)


def analyze():
    pass


def day(args, unknown, arg_parser=None, **kwargs):
    # TODO: rda.csv argument
    day_path = os.path.expanduser(unknown[0])
    day_csv = open(day_path)
    rda_csv = None
    if len(unknown) > 1:
        rda_path = os.path.expanduser(unknown[1])
        rda_csv = open(rda_path)
    return day_analyze(day_csv, rda_csv=rda_csv)
