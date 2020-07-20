#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:13:45 2020

@author: shane
"""

from .usda import (
    list_nutrients,
    sort_foods_by_kcal_nutrient_id,
    sort_foods_by_nutrient_id,
)


def nutrients(args, unknown, arg_parser=None):
    return list_nutrients()


def search():
    pass


def sort(args, unknown, arg_parser=None):
    # TODO: --kcal or -c, option for sorting by kcal
    print(args)
    return sort_foods_by_nutrient_id(789)


def analyze():
    pass
