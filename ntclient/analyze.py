# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 23:57:03 2018

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

import json

import requests
from tabulate import tabulate

from .utils.settings import SERVER_HOST


def cmd_analyze(args, unknown, arg_parser=None):
    # if args.r:
    #     print(f"recipe id: {args.r}")
    if not unknown:
        arg_parser.print_help()
        return

    # Get analysis
    food_ids = [int(x) for x in unknown]
    food_ids = ",".join([str(x) for x in food_ids])
    response = requests.get(
        f"{SERVER_HOST}/foods/analyze", params={"food_ids": food_ids}
    )
    analyses = response.json()["data"]
    # Get RDAs
    response = requests.get(f"{SERVER_HOST}/nutrients")
    rdas = response.json()["data"]
    rdas = {rda["id"]: rda for rda in rdas}

    # print(json.dumps(rdas))
    # print(json.dumps(analyses))
    # print(len(analyses))
    # print(rdas)

    for food in analyses:
        print(
            "\n======================================\n"
            f"==> {food['long_desc']} ({food['food_id']})\n"
            "======================================\n",
        )
        headers = ["nutrient", "amount", "units", "rda"]
        rows = []
        food_nutes = {x["nutr_id"]: x for x in food["nutrients"]}
        for id, nute in food_nutes.items():
            if not rdas[id]["rda"]:
                continue

            amount = food_nutes[id]["nutr_val"]
            if not amount:
                continue
            rda_ratio = round(amount / rdas[id]["rda"] * 100, 1)
            rows.append([nute["nutr_desc"], amount, rdas[id]["units"], f"{rda_ratio}%"])
        print(tabulate(rows, headers=headers, tablefmt="orgtbl"))
        # print(food["food_id"])
