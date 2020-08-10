#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:16:08 2020

@author: shane
"""

from tabulate import tabulate

from .utils.settings import SEARCH_LIMIT
from .utils.sqlfuncs import (
    fdgrp,
    nutrients_details,
    nutrients_overview,
    sort_foods,
    sort_foods_by_kcal,
)


def list_nutrients():

    headers, nutrients = nutrients_details()

    table = tabulate(nutrients, headers=headers, tablefmt="presto")
    print(table)
    return nutrients


def sort_foods_by_nutrient_id(id, by_kcal=False):
    results = sort_foods(id)
    results = [list(x) for x in results][:SEARCH_LIMIT]

    nutrients = nutrients_overview()
    nutrient = nutrients[id]
    unit = nutrient[2]

    fdgrps = fdgrp()

    headers = ["food_id", "fdgrp", f"value ({unit})", "kcal", "long_desc"]
    for x in results:
        _fdgrp = fdgrps[x[1]]
        x.insert(1, _fdgrp[1])

    table = tabulate(results, headers=headers, tablefmt="presto")
    print(table)
    return results


def sort_foods_by_kcal_nutrient_id(id):
    results = sort_foods_by_kcal(id)
    results = [list(x) for x in results][:SEARCH_LIMIT]

    nutrients = nutrients_overview()
    nutrient = nutrients[id]
    unit = nutrient[2]

    fdgrps = fdgrp()

    headers = ["food_id", "fdgrp_desc", "fdgrp", f"value ({unit})", "kcal", "long_desc"]
    for x in results:
        _fdgrp = fdgrps[x[1]]
        x.insert(1, _fdgrp[1])

    table = tabulate(results, headers=headers, tablefmt="presto")
    print(table)
    return results
