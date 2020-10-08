import os
import sqlite3

from .. import profile_id

# Set the usda.sqlite target version here
__db_target_nt__ = "0.0.0"

# Connect to DB
db_path = os.path.expanduser("~/.nutra/nt/nt.sqlite")
if os.path.isfile(db_path):
    conn = sqlite3.connect(db_path)
else:
    print("error: nt database doesn't exist, please run init")
    print("warn: init not implemented, manually build db with ntsqlite README")
    exit()


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
    return result[-1]


# TODO: Verify version
__db_version_nt__ = dbver()[1]

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


# ----------------------------
# Profile and Sync functions
# ----------------------------


def sql_profile_guid_from_id(profile_id):
    query = f"SELECT guid FROM profiles WHERE id={profile_id}"
    return _sql(query)[0][0]


# # Runs in __init__
# profile_guid = sql_profile_guid_from_id(profile_id)


def sql_last_sync():
    query = """
SELECT
  max(
    (SELECT IFNULL(max(last_sync), -1) FROM profiles),
    (SELECT IFNULL(max(last_sync), -1) FROM biometric_log),
    (SELECT IFNULL(max(last_sync), -1) FROM recipes),
    (SELECT IFNULL(max(last_sync), -1) FROM food_log),
    (SELECT IFNULL(max(last_sync), -1) FROM recipe_log),
    (SELECT IFNULL(max(last_sync), -1) FROM rda)
  ) AS last_sync;
"""
    return _sql(query)[0][0]


def sql_inserted_or_updated_entities(last_sync):
    query = f"SELECT * FROM profiles WHERE updated>{last_sync}"
    profiles = _sql(query)
    query = f"SELECT * FROM biometric_log WHERE updated>{last_sync}"
    bio_logs = _sql(query)

    return profiles, bio_logs


# ----------------------
# Biometric functions
# ----------------------


def sql_biometrics():
    query = "SELECT * FROM biometrics;"
    return _sql(query, headers=True)


def sql_biometric_logs(profile_id):
    query = "SELECT * FROM biometric_log WHERE profile_id=?"
    return _sql(query, args=(profile_id,), headers=True)


def sql_biometric_add(bio_vals):
    cur = conn.cursor()

    # TODO: finish up
    query1 = "INSERT INTO biometric_log(profile_id, tags, notes) VALUES (?, ?, ?)"
    result = _sql(query1, (profile_id, "", ""))
    id = cur.lastrowid
    print(id)
