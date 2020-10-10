#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 21:23:47 2020

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

import os
import shutil
import sqlite3
import sys
import tarfile
import time
import urllib.request

from ... import __db_target_usda__


# Onboarding function
def verify_db(__db_target_usda__, force_install=False):
    cwd = os.path.expanduser("~/.nutra/usda")

    # TODO: put this in main __init__? Require License agreement?
    if not os.path.exists(cwd):
        print("mkdir -p ~/.nutra/usda")
        os.makedirs(cwd, mode=0o755)

    if "usda.sqlite" not in os.listdir(cwd) or force_install:
        """Downloads and unpacks the nt-sqlite3 db"""

        def reporthook(count, block_size, total_size):
            """Shows download progress"""
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

        # Download usda.sqlite.tar.xz
        url = f"https://bitbucket.org/dasheenster/nutra-utils/downloads/usda.sqlite-{__db_target_usda__}.tar.xz"
        print(f"curl -L {url} -o usda.sqlite.tar.xz")
        urllib.request.urlretrieve(
            url, f"{cwd}/usda.sqlite.tar.xz", reporthook,
        )
        print()

        # Extract the archive
        # NOTE: in sql.__init__() we verify version == __db_target_usda__, and if needed invoke this method with force_install=True
        with tarfile.open(f"{cwd}/usda.sqlite.tar.xz", mode="r:xz") as f:
            try:
                print("tar xvf usda.sqlite.tar.xz")
                f.extractall(cwd)
            except Exception as e:
                print(repr(e))
                print("ERROR: corrupt tarball, removing. Please try the download again")
                print("rm -rf ~/.nutra/usda")
                shutil.rmtree(cwd)
                exit()
        print("==> done downloading usda.sqlite")


verify_db(__db_target_usda__)

# Connect to DB
# TODO: support as parameter in prefs.json or nt.sqlite ?
db_path = os.path.expanduser("~/.nutra/usda/usda.sqlite")
conn = sqlite3.connect(db_path)
# conn.row_factory = sqlite3.Row  # see: https://chrisostrouchov.com/post/python_sqlite/
c = conn.cursor()


def _sql(query, headers=False):
    """Executes a SQL command to usda.sqlite"""
    # TODO: DEBUG flag in properties.csv ... Print off all queries
    result = c.execute(query)
    rows = result.fetchall()
    if headers:
        headers = [x[0] for x in result.description]
        return headers, rows
    return rows


# ----------------------
# SQL internal functions
# ----------------------


def dbver():
    query = "SELECT * FROM version;"
    result = _sql(query)
    return result[-1]


# Verify version
try:
    __db_version_usda__ = dbver()[1]
    if __db_target_usda__ != __db_version_usda__:
        print(
            f"NOTE: target db ({__db_target_usda__}) differs from current ({__db_version_usda__}).. downloading target"
        )
        verify_db(__db_target_usda__, force_install=True)
        print("NOTE: please run your command again now")
        exit()
except Exception as e:
    print(repr(e))
    print("ERROR: corrupt databasde.. downloading fresh")
    verify_db(__db_target_usda__, force_install=True)
    print("NOTE: please run your command again now")
    exit()


# ----------------------
# SQL nutra functions
# ----------------------


def nutrients_overview():
    query = "SELECT * FROM nutr_def;"
    result = _sql(query)
    return {x[0]: x for x in result}


def fdgrp():
    query = "SELECT * FROM fdgrp;"
    result = _sql(query)
    return {x[0]: x for x in result}


def nutrients_details():
    """Nutrient details"""
    query = """
SELECT
  id,
  rda,
  unit,
  tagname,
  nutr_desc,
  COUNT(nut_data.nutr_id) AS n_foods,
  ROUND(avg(nut_data.nutr_val), 3) AS avg_val
FROM
  nutr_def
  INNER JOIN nut_data ON nut_data.nutr_id = id
GROUP BY
  id
ORDER BY
  id;
"""
    return _sql(query, headers=True)


def servings(food_ids):
    """Food servings"""
    # TODO: apply connective logic from `sort_foods()` IS ('None') ?
    query = """
SELECT
  serv.food_id,
  serv.msre_id,
  serv_desc.msre_desc,
  serv.grams
FROM
  serving serv
  LEFT JOIN serv_desc ON serv.msre_id = serv_desc.id
WHERE
  serv.food_id IN (%s);
"""
    food_ids = ",".join(str(x) for x in set(food_ids))
    return _sql(query % food_ids)


def analyze_foods(food_ids):
    """Nutrient analysis for foods"""
    query = """
SELECT
  id,
  nutr_id,
  nutr_val
FROM
  food_des
  INNER JOIN nut_data ON food_des.id = nut_data.food_id
WHERE
  food_des.id IN (%s);
"""
    food_ids = ",".join(str(x) for x in set(food_ids))
    return _sql(query % food_ids)


def food_details(food_ids):
    """Readable human details for foods"""
    query = "SELECT * FROM food_des WHERE id in (%s)"
    food_ids = ",".join(str(x) for x in set(food_ids))
    return _sql(query % food_ids)


def sort_foods(nutr_id, fdgrp_ids=None):
    """Sort foods by nutr_id per 100 g"""
    query = """
SELECT
  nut_data.food_id,
  fdgrp_id,
  nut_data.nutr_val,
  kcal.nutr_val AS kcal,
  long_desc
FROM
  nut_data
  INNER JOIN food_des food ON food.id = nut_data.food_id
  INNER JOIN nutr_def ndef ON ndef.id = nut_data.nutr_id
  INNER JOIN fdgrp ON fdgrp.id = fdgrp_id
  LEFT JOIN nut_data kcal ON food.id = kcal.food_id
    AND kcal.nutr_id = 208
WHERE
  nut_data.nutr_id = {0}"""
    if fdgrp_ids:
        query += """
  AND (fdgrp_id IN ({1}))"""
    query += """
ORDER BY
  nut_data.nutr_val DESC;"""
    if fdgrp_ids:
        fdgrp_ids = ",".join([str(x) for x in set(fdgrp_ids)])
        return _sql(query.format(nutr_id, fdgrp_ids))
    return _sql(query.format(nutr_id))


def sort_foods_by_kcal(nutr_id, fdgrp_ids=None):
    """Sort foods by nutr_id per 200 kcal"""
    query = """
SELECT
  nut_data.food_id,
  fdgrp_id,
  ROUND((nut_data.nutr_val * 200 / kcal.nutr_val), 2) AS nutr_val,
  kcal.nutr_val AS kcal,
  long_desc
FROM
  nut_data
  INNER JOIN food_des food ON food.id = nut_data.food_id
  INNER JOIN nutr_def ndef ON ndef.id = nut_data.nutr_id
  INNER JOIN fdgrp ON fdgrp.id = fdgrp_id
  -- filter out NULL kcal
  INNER JOIN nut_data kcal ON food.id = kcal.food_id
    AND kcal.nutr_id = 208
    AND kcal.nutr_val > 0
WHERE
  nut_data.nutr_id = {0}"""
    if fdgrp_ids:
        query += """
  AND (fdgrp_id IN ({1}))"""
    query += """
ORDER BY
  (nut_data.nutr_val / kcal.nutr_val) DESC;"""
    if fdgrp_ids:
        fdgrp_ids = ",".join([str(x) for x in set(fdgrp_ids)])
        return _sql(query.format(nutr_id, fdgrp_ids))
    return _sql(query.format(nutr_id))
