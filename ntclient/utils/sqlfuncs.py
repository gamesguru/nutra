#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 21:23:47 2020

@author: shane
"""

import os
import sqlite3

os.chdir(os.path.dirname(os.path.abspath(__file__)))
conn = sqlite3.connect("nutra.db")
# conn.row_factory = sqlite3.Row  # see: https://chrisostrouchov.com/post/python_sqlite/
c = conn.cursor()


def _sql(query):
    result = c.execute(query)
    keys = [x[0] for x in result.description]
    return keys, result.fetchall()


def nutrients():
    """Nutrient details"""
    query = """
SELECT
  id,
  nutr_desc,
  rda,
  unit,
  tagname,
  anti_nutrient,
  COUNT(nut_data.nutr_id) AS food_count,
  ROUND(avg(nut_data.nutr_val), 3) AS avg_val
FROM
  nutr_def
  INNER JOIN nut_data ON nut_data.nutr_id = id
GROUP BY
  id
ORDER BY
  id;
"""
    return _sql(query)


def servings(food_ids_in=None):
    """Food servings"""
    query = """
SELECT
  serv.food_id,
  serv.msre_id,
  serv_desc.msre_desc,
  serv.grams
FROM
  serving serv
  LEFT JOIN serv_desc ON serv.msre_id = serv_desc.id"""
    if food_ids_in:
        food_ids_in = ", ".join(str(x) for x in set(food_ids_in))
        query += """
WHERE
  serv.food_id IN (%s);
"""
        return _sql(query % food_ids_in)
    return _sql(query)


def analyze_foods(food_ids_in):
    """Nutrient analysis for foods"""
    food_ids_in = ", ".join(str(x) for x in set(food_ids_in))
    query = """
SELECT
  id,
  nutr_id,
  nutr_val
FROM
  food_des des
  INNER JOIN nut_data ON des.id = nut_data.food_id
WHERE
  des.id IN (%s);
"""
    return _sql(query % food_ids_in)


def food_details(food_ids_in):
    """Readable human details for foods"""
    food_ids_in = ", ".join(str(x) for x in set(food_ids_in))
    query = "SELECT * FROM food_des WHERE id in (%s)"
    return _sql(query % food_ids_in)
