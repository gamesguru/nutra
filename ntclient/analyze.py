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

import csv

import requests
from tabulate import tabulate

from .utils import remote
from .utils.settings import SERVER_HOST


def foods_analyze(food_ids):
    """Analyze a list of food_ids against stock RDA values"""

    # Get analysis
    food_ids = ",".join([str(x) for x in food_ids])
    response = requests.get(
        f"{SERVER_HOST}/foods/analyze", params={"food_ids": food_ids}
    )
    res = response.json()["data"]
    analyses = res["analyses"]
    servings = res["servings"]
    food_des = res["food_des"]

    # Get RDAs
    response = requests.get(f"{SERVER_HOST}/nutrients")
    rdas = response.json()["data"]
    rdas = {rda["id"]: rda for rda in rdas}

    # --------------------------------------
    # Food-by-food analysis (w/ servings)
    # --------------------------------------
    servings_tables = []
    nutrients_tables = []
    for food in analyses:
        food_id = food["food_id"]
        food_name = food["long_desc"]
        print(
            "\n======================================\n"
            f"==> {food_name} ({food_id})\n"
            "======================================\n",
        )
        print("\n=========================\nSERVINGS\n=========================\n")

        ###############
        # Serving table
        headers = ["msre_id", "msre_desc", "grams"]
        # Copy obj with dict(x)
        rows = [dict(x) for x in servings if x["food_id"] == food_id]
        for r in rows:
            r.pop("food_id")
        # Print table
        servings_table = tabulate(rows, headers="keys", tablefmt="presto")
        print(servings_table)
        servings_tables.append(servings_table)

        refuse = next(
            (x for x in food_des if x["id"] == food_id and x["ref_desc"]), None
        )
        if refuse:
            print("\n=========================\nREFUSE\n=========================\n")
            print(refuse["ref_desc"])
            print(f"    ({refuse['refuse']}%, by mass)")

        print("\n=========================\nNUTRITION\n=========================\n")

        ################
        # Nutrient table
        headers = ["id", "nutrient", "amount", "units", "rda"]
        rows = []
        food_nutes = {x["nutr_id"]: x for x in food["nutrients"]}
        for id, nute in food_nutes.items():
            # Skip zero values
            amount = food_nutes[id]["nutr_val"]
            if not amount:
                continue

            # Insert RDA % into row
            if rdas[id]["rda"]:
                rda_ratio = round(amount / rdas[id]["rda"] * 100, 1)
                row = [
                    id,
                    nute["nutr_desc"],
                    amount,
                    rdas[id]["units"],
                    f"{rda_ratio}%",
                ]
            else:
                # print(rdas[id])
                row = [id, nute["nutr_desc"], amount, rdas[id]["units"], None]

            rows.append(row)

        # Print table
        nutrients = tabulate(rows, headers=headers, tablefmt="presto")
        print(nutrients)
        nutrients_tables.append(nutrients)

    return nutrients_tables, servings_tables


def day_analyze(day_csv_paths, rda_csv_path=None):
    """Analyze a day optionally with custom RDAs,
    e.g.  nutra day ~/.nutra/rocky.csv -r ~/.nutra/dog-rdas-18lbs.csv
    TODO: Should be a subset of foods_analyze
    """

    analyses = []
    for day_csv_path in day_csv_paths:
        day_csv_input = csv.DictReader(open(day_csv_path))

        log = []
        for row in day_csv_input:
            log.append(row)

        rda = []
        if rda_csv_path:
            rda_csv_input = csv.DictReader(open(rda_csv_path))
            for row in rda_csv_input:
                rda.append(row)

        response = remote.request("/day/analyze", body={"log": log, "rda": rda})
        results = response.json()["data"]
        # TODO: if err

        totals = results["nutrient_totals"]
        print(totals)
        analyses.append(totals)
    return analyses
