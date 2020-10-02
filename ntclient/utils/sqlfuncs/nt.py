import os
import sqlite3

# Connect to DB
db_path = os.path.expanduser("~/.nutra/nt/nt.sqlite")
conn = sqlite3.connect(db_path)
c = conn.cursor()


def _sql(query, args=None, headers=False):
    """Executes a SQL command to usda.sqlite"""
    # TODO: DEBUG flag in properties.csv ... Print off all queries
    if args:
        if type(args) == list:
            result = c.executemany(query, args)
        else:
            result = c.execute(query, args)
    else:
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
    return _sql(query, id)


def biometrics():
    query = "SELECT * FROM biometrics;"
    return _sql(query)


def biometric_add(bio_vals):
    # TODO: get current user_id from __init__.py
    user_id = 1
    query1 = "INSERT INTO biometric_log(user_id, tags, notes) VALUES (?, ?, ?) RETURNING id;"
    result = _sql(query1, (user_id, "", ""))
    print(result)

