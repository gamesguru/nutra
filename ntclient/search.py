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

import shutil

from tabulate import tabulate

from .utils import remote
from .utils.settings import NUTR_ID_KCAL, NUTR_IDS_AMINOS, NUTR_IDS_FLAVONES


def cmd_search(args, unknown, arg_parser=None):
    return search(words=unknown)


def search(words, dbs=None):
    """ Searches all dbs, foods, recipes, recents and favorites. """
    params = dict(terms=",".join(words))

    response = remote.request("/foods/search", params=params)
    results = response.json()["data"]

    print_results(results)


def print_results(results):
    # Current terminal size
    # TODO: dynamic buffer
    # TODO: display "nonzero/total" report nutrients, aminos, and flavones.. sometimes zero values are not useful
    # bufferwidth = shutil.get_terminal_size()[0]
    bufferheight = shutil.get_terminal_size()[1]

    headers = [
        "food_id",
        "food_name",
        "kcal",
        "# nutrients",
        "Aminos",
        "Flavones",
        "fdgrp_desc",
    ]
    rows = []
    for i, r in enumerate(results):
        if i == bufferheight - 4:
            break
        food_id = r["food_id"]
        food_name = r["long_desc"][:45]
        fdgrp_desc = r["fdgrp_desc"]

        nutrients = r["nutrients"]
        kcal = nutrients.get(str(NUTR_ID_KCAL))
        kcal = kcal["nutr_val"] if kcal else None
        len_aminos = len(
            [nutrients[n_id] for n_id in nutrients if int(n_id) in NUTR_IDS_AMINOS]
        )
        len_flavones = len(
            [nutrients[n_id] for n_id in nutrients if int(n_id) in NUTR_IDS_FLAVONES]
        )

        row = [
            food_id,
            food_name,
            kcal,
            len(nutrients),
            len_aminos,
            len_flavones,
            fdgrp_desc,
        ]
        rows.append(row)
        # avail_buffer = bufferwidth - len(food_id) - 15
        # if len(food_name) > avail_buffer:
        #     rows.append([food_id, food_name[:avail_buffer] + "..."])
        # else:
        #     rows.append([food_id, food_name])
    print(tabulate(rows, headers=headers, tablefmt="orgtbl"))
