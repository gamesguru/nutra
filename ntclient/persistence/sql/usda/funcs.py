from . import con, _sql, verify_usda, __db_target_usda__


def usda_ver():
    """Gets version string for usda.sqlite database"""
    if con is None:
        return None
    query = "SELECT * FROM version;"
    result = _sql(query)
    return result[-1][1]


# Verify version
# try:
#     __db_version_usda__ = usda_ver()
#     if __db_target_usda__ != __db_version_usda__:
#         print(
#             f"NOTE: target db ({__db_target_usda__}) differs from current ({__db_version_usda__}).. downloading target"
#         )
#         verify_usda(__db_target_usda__, force_install=True)
#         print("NOTE: please run your command again now")
#         exit()
# except Exception as e:
#     print(repr(e))
#     print("ERROR: corrupt database.. downloading fresh")
#     verify_usda(__db_target_usda__, force_install=True)
#     print("NOTE: please run your command again now")
#     exit()


# ----------------------
# USDA  functions
# ----------------------


def fdgrp():
    query = "SELECT * FROM fdgrp;"
    result = _sql(query)
    return {x[0]: x for x in result}


def food_details(food_ids):
    """Readable human details for foods"""
    query = "SELECT * FROM food_des WHERE id in (%s)"
    food_ids = ",".join(str(x) for x in set(food_ids))
    return _sql(query % food_ids)


def nutrients_overview():
    query = "SELECT * FROM nutr_def;"
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
