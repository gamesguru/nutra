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
    response = requests.get(f"{SERVER_HOST}/analyze", params={"food_ids": food_ids})
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


# def analyze(PK_No=None, grams=100):
#     dbs = db.fdbs()
#     for d in dbs:
#         for e in d.fdb_entries:
#             if e.pk_no == PK_No:
#                 print(f"Analyze: {e.foodname} ({grams}g)\n")

#                 # Prints basic fields
#                 max_basic_length = 0
#                 # TODO: this
#                 # for f in e.fields
#                 # Prints relative fields
#                 max_rel_length = 0
#                 for r in d.rels:
#                     for re in r.rel_entries:
#                         if re.pk_no == PK_No:
#                             if float(re.nutramt) == 0.0:
#                                 continue
#                             max_rel_length = (
#                                 max_rel_length
#                                 if max_rel_length > len(re.nutrname)
#                                 else len(re.nutrname)
#                             )
#                             # print(f'{re.nutrname} @ {re.nutramt}')
#                 for r in d.rels:
#                     for re in r.rel_entries:
#                         if re.pk_no == PK_No:
#                             reamt = round(float(re.nutramt) * grams / 100, 2)
#                             if reamt == 0.0:
#                                 continue
#                             pad_rel_name = re.nutrname + " " * (
#                                 max_rel_length - len(re.nutrname)
#                             )
#                             print(f"{pad_rel_name}  {reamt} mg")


# def main(args=None):
#     if args == None:
#         args = sys.argv

#     # No arguments passed in
#     if len(args) == 0:
#         print(usage)

#     # Otherwise we have some args
#     for i, arg in enumerate(args):
#         rarg = args[i:]
#         if hasattr(cmdmthds, arg):
#             getattr(cmdmthds, arg).mthd(rarg[1:])
#             break
#         # Activate method for opt commands, e.g. `-h' or `--help'
#         elif altcmd(i, arg) != None:
#             altcmd(i, arg)(rarg[1:])
#             break
#         # Otherwise we don't know the arg
#         else:
#             print(f"error: unknown option `{arg}'.  See 'nutra anl --help'.")
#             break


# def altcmd(i, arg):
#     for i in inspect.getmembers(cmdmthds):
#         for i2 in inspect.getmembers(i[1]):
#             if i2[0] == "altargs" and arg in i2[1]:
#                 return i[1].mthd
#     return None


# class cmdmthds:
#     """ Where we keep the `cmd()` methods && opt args """

#     class dbno:
#         def mthd(rarg):
#             if len(rarg) != 1 and len(rarg) != 2:
#                 exit(
#                     f"error: must specify only one PK_No, optionally followed by an amount in grams"
#                 )
#             try:
#                 PK_No = int(rarg[0])
#             except:
#                 exit("error: invalid integer number for PK_No")
#             try:
#                 grams = int(rarg[1])
#             except:
#                 print("warn: no grams provided, using 100g")
#                 grams = 100
#             analyze(PK_No, grams)

#         altargs = ["-n"]

#     class help:
#         def mthd(rarg):
#             print(usage)

#         altargs = ["-h", "--help"]


# usage = f"""Analyze ingredients, foods, recipes, and days.
# Version {version}

# Usage: nutra anl <option> [<value>]

# Options:
#     dbno | -n  analyze an ingredient by PK_No (NDB_No)"""
