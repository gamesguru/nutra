import os
import sqlite3

# Connect to DB
db_path = os.path.expanduser("~/.nutra/nt/nt.sqlite")
conn = sqlite3.connect(db_path)
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
    return result[-1][1]


# ----------------------
# SQL nutra functions
# ----------------------


def recipes():
    query = """
SELECT
  id,
  name,
  (
    SELECT
      COUNT()
    FROM
      recipe_dat
    WHERE
      recipe_id = recipes.id) AS n_foods,
  (
    SELECT
      SUM(grams)
    FROM
      recipe_dat
    WHERE
      recipe_id = recipes.id) AS weight,
  guid,
  created
FROM
  recipes;
"""
    return _sql(query, headers=True)
