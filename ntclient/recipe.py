#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:14:00 2020

@author: shane
"""

from tabulate import tabulate

from .utils.sqlfuncs.nt import recipes as _recipes

# from .utils.sqlfuncs.usda import analyze_foods


def recipes_overview():
    recipes = _recipes()[1]

    results = []
    for recipe in recipes:
        result = {
            "id": recipe[0],
            "name": recipe[1],
            "n_foods": recipe[2],
            "weight": recipe[3],
            "guid": recipe[4],
            "created": recipe[5],
        }
        results.append(result)

    table = tabulate(results, headers="keys", tablefmt="presto")
    print(table)
    return results


def recipe_analyze(id):
    recipes = _recipes()

    try:
        recipe = recipes[id]
    except Exception as e:
        print(repr(e))
        return None

    id = recipe[0]
    name = recipe[1]
    # foods = {x[0]: x[1] for x in recipe[3]}
    # analyses = analyze_foods(foods)
    print(f"{name}\n")
    print("work in progress.. check back later.. need to re-use foods-analysis format")
    return recipe
