#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 21:23:47 2020

@author: shane
"""

import lzma
import os
import sqlite3
import sys
import tarfile
import time
import urllib.request

os.chdir(os.path.expanduser("~/.nutra"))
if "nutra.db" not in os.listdir():
    """Downloads and unpacks the nt-sqlite3 db"""

    def reporthook(count, block_size, total_size):
        """ Shows download progress """
        global start_time
        if count == 0:
            start_time = time.time()
            time.sleep(0.01)
            return
        duration = time.time() - start_time
        progress_size = int(count * block_size)
        speed = int(progress_size / (1024 * duration))
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write(
            "\r...%d%%, %d MB, %d KB/s, %d seconds passed"
            % (percent, progress_size / (1024 * 1024), speed, duration)
        )
        sys.stdout.flush()

    if "nutra.db.tar.xz" not in os.listdir():
        # Download nutra.db.tar.xz
        file = urllib.request.urlretrieve(
            "https://bitbucket.org/dasheenster/nutra-utils/downloads/nutra.db.tar.xz",
            "nutra.db.tar.xz",
            reporthook,
        )
    # Extract
    with tarfile.open("nutra.db.tar.xz", mode="r:xz") as f:
        f.extractall()
    print("==> done downloading nutra.db")

# Connect to DB
conn = sqlite3.connect("nutra.db")
# conn.row_factory = sqlite3.Row  # see: https://chrisostrouchov.com/post/python_sqlite/
c = conn.cursor()


def _sql(query):
    """Executes a SQL command to nutra.db"""
    result = c.execute(query)
    keys = [x[0] for x in result.description]
    return keys, result.fetchall()


# ----------------------
# SQL syntax functions
# ----------------------


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
