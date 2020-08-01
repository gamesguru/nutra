# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 23:57:03 2018

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutraent analysis and composition application.
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

import csv
import shutil

import requests
from colorama import Fore, Style
from tabulate import tabulate

from .utils import remote
from .utils.settings import (
    COLOR_CRIT,
    COLOR_DEFAULT,
    COLOR_OVER,
    COLOR_WARN,
    NUTR_ID_CARBS,
    NUTR_ID_FAT_TOT,
    NUTR_ID_FIBER,
    NUTR_ID_KCAL,
    NUTR_ID_PROTEIN,
    SERVER_HOST,
    THRESH_CRIT,
    THRESH_OVER,
    THRESH_WARN,
)


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

    rda = []
    if rda_csv_path:
        rda_csv_input = csv.DictReader(open(rda_csv_path))
        for row in rda_csv_input:
            rda.append(row)

    logs = []
    analyses = []
    for day_csv_path in day_csv_paths:
        day_csv_input = csv.DictReader(open(day_csv_path))
        log = list(day_csv_input)
        logs.append(log)

    response = remote.request("/day/analyze", body={"logs": logs, "rda": rda})
    results = response.json()["data"]
    # TODO: if err
    totals = results["nutrients_totals"]
    nutrients = results["nutrients"]

    # JSON doesn't support int keys
    analyses = [{int(k): v for k, v in total.items()} for total in totals]
    nutrients = {int(k): v for k, v in nutrients.items()}

    #######
    # Print
    w = shutil.get_terminal_size()[0]
    buffer = w - 4 if w > 4 else w
    for analysis in analyses:
        day_format(analysis, nutrients, buffer=buffer)
    return analyses


def day_format(analysis, nutrients, buffer=None):
    def print_header(header):
        print(Fore.CYAN, end="")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"→ {header}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(Style.RESET_ALL)

    def print_macro_bar(fat, net_carb, pro, kcals_max, buffer=None):
        kcals = fat * 9 + net_carb * 4 + pro * 4

        p_fat = (fat * 9) / kcals
        p_carb = (net_carb * 4) / kcals
        p_pro = (pro * 4) / kcals

        # TODO: handle rounding cases, tack on to, or trim off FROM LONGEST ?
        mult = kcals / kcals_max
        n_fat = round(p_fat * buffer * mult)
        n_carb = round(p_carb * buffer * mult)
        n_pro = round(p_pro * buffer * mult)

        # Headers
        f_buf = " " * (n_fat // 2) + "Fat" + " " * (n_fat - n_fat // 2 - 3)
        c_buf = " " * (n_carb // 2) + "Carbs" + " " * (n_carb - n_carb // 2 - 5)
        p_buf = " " * (n_pro // 2) + "Pro" + " " * (n_pro - n_pro // 2 - 3)
        print(
            f"  {Fore.YELLOW}{f_buf}{Fore.BLUE}{c_buf}{Fore.RED}{p_buf}{Style.RESET_ALL}"
        )

        # Bars
        print(" <", end="")
        print(Fore.YELLOW + "=" * n_fat, end="")
        print(Fore.BLUE + "=" * n_carb, end="")
        print(Fore.RED + "=" * n_pro, end="")
        print(Style.RESET_ALL + ">")

        # Calorie footers
        k_fat = str(round(fat * 9))
        k_carb = str(round(net_carb * 4))
        k_pro = str(round(pro * 4))
        f_buf = " " * (n_fat // 2) + k_fat + " " * (n_fat - n_fat // 2 - len(k_fat))
        c_buf = (
            " " * (n_carb // 2) + k_carb + " " * (n_carb - n_carb // 2 - len(k_carb))
        )
        p_buf = " " * (n_pro // 2) + k_pro + " " * (n_pro - n_pro // 2 - len(k_pro))
        print(
            f"  {Fore.YELLOW}{f_buf}{Fore.BLUE}{c_buf}{Fore.RED}{p_buf}{Style.RESET_ALL}"
        )

    def print_nute_bar(n_id, amount, nutrients):
        n = nutrients[n_id]
        rda = n.get("rda")
        tag = n["tagname"]
        unit = n["units"]
        anti = n["anti_nutrient"]

        if not rda:
            return False, n
        attain = amount / rda
        perc = round(100 * attain, 1)

        if attain >= THRESH_OVER:
            color = COLOR_OVER
        elif attain <= THRESH_CRIT:
            color = COLOR_CRIT
        elif attain <= THRESH_WARN:
            color = COLOR_WARN
        else:
            color = COLOR_DEFAULT

        # Print
        detail_amount = f"{round(amount, 1)}/{rda} {unit}".ljust(18)
        detail_amount = f"{detail_amount} -- {tag}"
        li = 20
        l = round(li * attain) if attain < 1 else li
        print(f" {color}<", end="")
        print("=" * l + " " * (li - l) + ">", end="")
        print(f" {perc}%\t[{detail_amount}]", end="")
        print(Style.RESET_ALL)

        return (True,)

    # Actual values
    kcals = round(analysis[NUTR_ID_KCAL])
    pro = analysis[NUTR_ID_PROTEIN]
    net_carb = analysis[NUTR_ID_CARBS] - analysis[NUTR_ID_FIBER]
    fat = analysis[NUTR_ID_FAT_TOT]
    kcals_449 = round(4 * pro + 4 * net_carb + 9 * fat)

    # Desired values
    kcals_rda = round(nutrients[NUTR_ID_KCAL]["rda"])
    pro_rda = nutrients[NUTR_ID_PROTEIN]["rda"]
    net_carb_rda = nutrients[NUTR_ID_CARBS]["rda"] - nutrients[NUTR_ID_FIBER]["rda"]
    fat_rda = nutrients[NUTR_ID_FAT_TOT]["rda"]

    # Print calories and macronutrient bars
    print_header("Macronutrients")
    kcals_max = max(kcals, kcals_rda)
    print(
        f"Actual:    {kcals} kcal ({round(kcals * 100 / kcals_rda, 1)}% RDA), {kcals_449} by 4-4-9"
    )
    print_macro_bar(fat, net_carb, pro, kcals_max, buffer=buffer)
    print(f"\nDesired:   {kcals_rda} kcal ({'%+d' % (kcals - kcals_rda)} kcal)")
    print_macro_bar(
        fat_rda, net_carb_rda, pro_rda, kcals_max, buffer=buffer,
    )

    # Nutrition detail report
    print_header("Nutrition detail report")
    for n_id in analysis:
        print_nute_bar(n_id, analysis[n_id], nutrients)
    # TODO: below
    print(
        "work in progress...some minor fields with negligible data, they are not shown here"
    )
