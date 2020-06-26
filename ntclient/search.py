# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 20:28:06 2018

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutraent analysis and composition application.
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
"""

import inspect
import shutil
import sys

from tabulate import tabulate

from . import remote


def cmd_search(args, unknown, arg_parser=None):
    return search(words=unknown)


def search(words, dbs=None):
    """ Searches all dbs, foods, recipes, recents and favorites. """
    params = dict(terms=",".join(words))

    response = remote.request("/foods/search", params=params)
    results = response.json()["data"]

    print_id_and_long_desc(results)


def print_id_and_long_desc(results):
    # Current terminal size
    bufferwidth = shutil.get_terminal_size()[0]
    bufferheight = shutil.get_terminal_size()[1]

    rows = []
    for i, r in enumerate(results):
        if i == bufferheight - 4:
            break
        food_id = str(r["food_id"])
        food_name = str(r["long_desc"])
        avail_buffer = bufferwidth - len(food_id) - 15
        if len(food_name) > avail_buffer:
            rows.append([food_id, food_name[:avail_buffer] + "..."])
        else:
            rows.append([food_id, food_name])
    print(tabulate(rows, headers=["food_id", "food_name"], tablefmt="orgtbl"))
