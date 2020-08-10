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

from fuzzywuzzy import fuzz
from tabulate import tabulate

from .utils.settings import (
    NUTR_ID_KCAL,
    NUTR_IDS_AMINOS,
    NUTR_IDS_FLAVONES,
    SEARCH_LIMIT,
)
from .utils.sqlfuncs import _sql, analyze_foods


def search_results(words):
    food_des = _sql("SELECT * FROM food_des;")

    query = " ".join(words)
    scores = {f[0]: fuzz.token_set_ratio(query, f[2]) for f in food_des}
    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:SEARCH_LIMIT]

    food_ids = [s[0] for s in scores]
    nut_data = analyze_foods(food_ids)

    # Tally foods
    foods_nutrients = {}
    for food_id, nutr_id, nutr_val in nut_data:
        if food_id not in foods_nutrients:
            foods_nutrients[food_id] = {nutr_id: nutr_val}  # init dict
        else:
            foods_nutrients[food_id][nutr_id] = nutr_val

    results = []
    food_des = {f[0]: f for f in food_des}
    for score in scores:
        food_id = score[0]
        score = score[1]

        food = food_des[food_id]
        fdgrp_id = food[1]
        long_desc = food[2]

        nutrients = foods_nutrients[food_id]
        result = {
            "food_id": food_id,
            "fdgrp_id": fdgrp_id,
            # TODO: get more details from another function, maybe enhance food_details() ?
            # "fdgrp_desc": cache.fdgrp[fdgrp_id]["fdgrp_desc"],
            # "data_src": cache.data_src[data_src_id]["name"],
            "long_desc": long_desc,
            "score": score,
            "nutrients": nutrients,
        }
        results.append(result)

    tabulate_search(results)


def tabulate_search(results):
    # Current terminal size
    # TODO: dynamic buffer
    # TODO: display "nonzero/total" report nutrients, aminos, and flavones.. sometimes zero values are not useful
    # TODO: macros, ANDI score, and other metrics on preview
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
        # food_name = r["long_desc"][:45]
        # food_name = r["long_desc"][:bufferwidth]
        food_name = r["long_desc"]
        # fdgrp_desc = r["fdgrp_desc"]
        fdgrp_desc = r["fdgrp_id"]

        nutrients = r["nutrients"]
        kcal = nutrients.get(NUTR_ID_KCAL)
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
    table = tabulate(rows, headers=headers, tablefmt="presto")
    print(table)
    return table
