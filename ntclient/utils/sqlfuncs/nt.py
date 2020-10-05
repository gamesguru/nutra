import os
import sqlite3

# Set the usda.sqlite target version here
__nt_db_target__ = "0.0.0"

# Connect to DB
db_path = os.path.expanduser("~/.nutra/nt/nt.sqlite")
conn = sqlite3.connect(db_path)


def _sql(query, args=None, headers=False):
    """Executes a SQL command to nt.sqlite"""
    cur = conn.cursor()

    # TODO: DEBUG flag in properties.csv ... Print off all queries
    if args:
        if type(args) == list:
            result = cur.executemany(query, args)
        else:  # tuple
            result = cur.execute(query, args)
    else:
        result = cur.execute(query)
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
    return result[-1][1]


# TODO: Verify version
__nt_db_version__ = dbver()

# ----------------------
# Recipe functions
# ----------------------


def recipe_add():
    query = """
"""
    return _sql(query)


def recipes():
    query = """
SELECT
  id,
  name,
  COUNT(recipe_id) AS n_foods,
  SUM(grams) AS grams,
  guid,
  created
FROM
  recipes
  LEFT JOIN recipe_dat ON recipe_id = id
GROUP BY
  id;
"""
    return _sql(query, headers=True)


def analyze_recipe(id):
    query = f"""
SELECT
  id,
  name,
  food_id,
  grams
FROM
  recipes
  INNER JOIN recipe_dat ON recipe_id = id
    AND id = {id};
"""
    return _sql(query)


def recipe(id):
    query = "SELECT * FROM recipes WHERE id=?;"
    return _sql(query, (id,))


# ----------------------
# Biometric functions
# ----------------------


def biometrics():
    query = "SELECT * FROM biometrics;"
    return _sql(query)


def biometric_logs(profile_id):
    query = "SELECT * FROM biometric_log WHERE profile_id=?"
    return _sql(query, args=(profile_id,), headers=True)


def biometric_add(bio_vals):
    cur = conn.cursor()
    # TODO: get current profile_id from __init__.py and admin.json
    profile_id = 1
    query1 = "INSERT INTO biometric_log(profile_id, tags, notes) VALUES (?, ?, ?)"
    result = _sql(query1, (profile_id, "", ""))
    id = cur.lastrowid
    print(id)
