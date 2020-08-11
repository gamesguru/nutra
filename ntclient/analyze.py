# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 23:57:03 2018

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

import csv
import shutil

from colorama import Fore, Style
from tabulate import tabulate

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
    TESTING,
    THRESH_CRIT,
    THRESH_OVER,
    THRESH_WARN,
    VERBOSITY,
)
from .utils.sqlfuncs import (
    analyze_foods,
    food_details,
    nutrients_overview,
    servings,
)


def foods_analyze(food_ids):
    """Analyze a list of food_ids against stock RDA values"""

    # Get analysis
    analysis = analyze_foods(food_ids)
    analyses = {}
    for a in analysis:
        id = a[0]
        anl = (a[1], a[2])
        if id not in analyses:
            analyses[id] = [anl]
        else:
            analyses[id].append(anl)
    # serving = servings()[1]
    serving = servings(food_ids)
    food_des = food_details(food_ids)
    food_des = {x[0]: x for x in food_des}
    nutrients = nutrients_overview()
    rdas = {x[0]: x[1] for x in nutrients.values()}

    # --------------------------------------
    # Food-by-food analysis (w/ servings)
    # --------------------------------------
    servings_tables = []
    nutrients_tables = []
    for food_id in analyses:
        food_name = food_des[food_id][2]
        # food_name = food["long_desc"]
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
        rows = [(x[1], x[2], x[3]) for x in serving if x[0] == food_id]
        # for r in rows:
        #     r.pop("food_id")
        # Print table
        servings_table = tabulate(rows, headers=headers, tablefmt="presto")
        print(servings_table)
        servings_tables.append(servings_table)

        refuse = next(
            ((x[7], x[8]) for x in food_des.values() if x[0] == food_id and x[7]), None
        )
        if refuse:
            print("\n=========================\nREFUSE\n=========================\n")
            print(refuse[0])
            print(f"    ({refuse[1]}%, by mass)")

        print("\n=========================\nNUTRITION\n=========================\n")

        ################
        # Nutrient table
        headers = ["id", "nutrient", "rda", "amount", "units"]
        rows = []
        # food_nutes = {x["nutr_id"]: x for x in food["nutrients"]}
        # for id, nute in food_nutes.items():
        for id, amount in analyses[food_id]:
            # Skip zero values
            # amount = food_nutes[id]["nutr_val"]
            if not amount:
                continue

            nutr_desc = nutrients[id][4] if nutrients[id][4] else nutrients[id][3]
            unit = nutrients[id][2]

            # Insert RDA % into row
            if rdas[id]:
                rda_perc = str(round(amount / rdas[id] * 100, 1)) + "%"
            else:
                # print(rdas[id])
                rda_perc = None
            row = [id, nutr_desc, rda_perc, round(amount, 2), unit]

            rows.append(row)

        # Print table
        table = tabulate(rows, headers=headers, tablefmt="presto")
        print(table)
        nutrients_tables.append(table)

    return nutrients_tables, servings_tables


def day_analyze(day_csv_paths, rda_csv_path=None):
    """Analyze a day optionally with custom RDAs,
    e.g.  nutra day ~/.nutra/rocky.csv -r ~/.nutra/dog-rdas-18lbs.csv
    TODO: Should be a subset of foods_analyze
    """
    rda = []
    if rda_csv_path:
        fp = open(rda_csv_path)
        rda_csv_input = csv.DictReader(row for row in fp if not row.startswith("#"))
        rda = list(rda_csv_input)

    logs = []
    food_ids = set()
    for day_csv_path in day_csv_paths:
        fp = open(day_csv_path)
        day_csv_input = csv.DictReader(row for row in fp if not row.startswith("#"))
        log = list(day_csv_input)
        for entry in log:
            try:
                food_ids.add(int(entry["id"]))
            except Exception as e:
                if TESTING or VERBOSITY > 1:
                    print(repr(e))
        logs.append(log)

    # Inject user RDAs
    nutrients = [list(x) for x in nutrients_overview().values()]
    for r in rda:
        id = int(r["id"])
        _rda = float(r["rda"])
        for n in nutrients:
            if n[0] == id:
                n[1] = _rda
                if VERBOSITY > 1:
                    print(f"INJECT RDA: {f'{_rda} {n[2]}'.ljust(12)} -->  {n[4]}")
    nutrients = {x[0]: x for x in nutrients}

    # Analyze foods
    _foods_analysis = analyze_foods(food_ids)
    foods_analysis = {}
    for f in _foods_analysis:
        id = f[0]
        anl = f[1], f[2]
        if id not in foods_analysis:
            foods_analysis[id] = [anl]
        else:
            foods_analysis[id].append(anl)

    # Compute totals
    nutrients_totals = []
    for log in logs:
        nutrient_totals = {}
        for entry in log:
            if entry["id"]:
                id = int(entry["id"])
                grams = float(entry["grams"])
                for n in foods_analysis[id]:
                    nutr_id = n[0]
                    nutr_per_100g = n[1]
                    nutr_val = grams / 100 * nutr_per_100g
                    if nutr_id not in nutrient_totals:
                        nutrient_totals[nutr_id] = nutr_val
                    else:
                        nutrient_totals[nutr_id] += nutr_val
        nutrients_totals.append(nutrient_totals)

    #######
    # Print
    w = shutil.get_terminal_size()[0]
    buffer = w - 4 if w > 4 else w
    for analysis in nutrients_totals:
        day_format(analysis, nutrients, buffer=buffer)
    return nutrients_totals


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
        nutrient = nutrients[n_id]
        rda = nutrient[1]
        tag = nutrient[3]
        unit = nutrient[2]
        anti = nutrient[5]

        if not rda:
            return False, nutrient
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
    kcals_rda = round(nutrients[NUTR_ID_KCAL][1])
    pro_rda = nutrients[NUTR_ID_PROTEIN][1]
    net_carb_rda = nutrients[NUTR_ID_CARBS][1] - nutrients[NUTR_ID_FIBER][1]
    fat_rda = nutrients[NUTR_ID_FAT_TOT][1]

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
