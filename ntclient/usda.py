#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:16:08 2020

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

    table = tabulate(nutrients, headers=headers, tablefmt="simple")
    print(table)
    return nutrients


def sort_foods_by_nutrient_id(id, by_kcal=False):
    results = sort_foods(id)
    results = [list(x) for x in results][:SEARCH_LIMIT]

    nutrients = nutrients_overview()
    nutrient = nutrients[id]
    unit = nutrient[2]

    headers = ["food", "fdgrp", f"val ({unit})", "kcal", "long_desc"]

    table = tabulate(results, headers=headers, tablefmt="simple")
    print(table)
    return results


def sort_foods_by_kcal_nutrient_id(id):
    results = sort_foods_by_kcal(id)
    results = [list(x) for x in results][:SEARCH_LIMIT]

    nutrients = nutrients_overview()
    nutrient = nutrients[id]
    unit = nutrient[2]

    headers = ["food", "fdgrp", f"val ({unit})", "kcal", "long_desc"]

    table = tabulate(results, headers=headers, tablefmt="simple")
    print(table)
    return results
