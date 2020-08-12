#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:14:00 2020

@author: shane
"""

import csv

from tabulate import tabulate

from .utils import NUTRA_DIR
from .utils.sqlfuncs import analyze_foods

cwd = f"{NUTRA_DIR}/recipe"


def parse_recipes():
    recipes = {}

    with open(f"{cwd}/names.csv") as f:
        csv_reader = csv.reader(f)
        rows = list(csv_reader)[1:]
        for id, tag, name in rows:
            id = int(id)
            recipes[id] = [id, tag, name]

    with open(f"{cwd}/food_amounts.csv") as f:
        csv_reader = csv.reader(f)
        rows = list(csv_reader)[1:]
        for row in rows:
            if row[0] == "":
                continue
            id = int(row[0])
            food_id = int(row[1])
            grams = float(row[2])
            recipe = recipes[id]
            if len(recipe) == 3:
                recipe.append([[food_id, grams]])
            else:
                recipe[3].append([food_id, grams])

    return recipes


def recipes_overview():
    recipes = parse_recipes()

    results = []
    for recipe in recipes.values():
        result = {
            "id": recipe[0],
            "tag": recipe[1],
            "name": recipe[2],
            "n_foods": len(recipe[3]),
        }
        results.append(result)

    table = tabulate(results, headers="keys", tablefmt="presto")
    print(table)
    return results


def recipe_analyze(id):
    recipes = parse_recipes()

    try:
        recipe = recipes[id]
    except Exception as e:
        print(repr(e))
        return None

    id = recipe[0]
    name = recipe[2]
    # foods = {x[0]: x[1] for x in recipe[3]}
    # analyses = analyze_foods(foods)
    print(f"{name} [id={id}]\n")
    print("work in progres.. check back later.. need to re-use foods-analysis format")
    return recipe
