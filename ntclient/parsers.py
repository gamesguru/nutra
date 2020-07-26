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


def nutrients(args, unknown, arg_parser=None):
    return list_nutrients()


def search():
    pass


def sort(args, unknown, arg_parser=None):
    by_kcal = args.kcal
    nutr_id = args.nutr_id
    return sort_foods_by_nutrient_id(nutr_id, by_kcal=by_kcal)


def analyze():
    pass


def day(args, unknown, arg_parser=None):
    # TODO: rda.csv argument
    day_path = os.path.expanduser(unknown[0])
    day_csv = open(day_path)
    rda_csv = None
    if len(unknown) > 1:
        rda_path = os.path.expanduser(unknown[1])
        rda_csv = open(rda_path)
    return day_analyze(day_csv, rda_csv=rda_csv)