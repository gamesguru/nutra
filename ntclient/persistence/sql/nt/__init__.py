import os
import sqlite3

from .... import __db_target_usda__
from ... import NUTRA_DIR

# Connect to DB
db_path = os.path.expanduser(f"{NUTRA_DIR}/nt/nt.sqlite")
if os.path.isfile(db_path):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
else:
    # print("warn: nt database doesn't exist, please run init")
    # print("info: init not implemented, manually build db with ntsqlite README")
    con = None


def _sql(query, args=None, headers=False):
    """Executes a SQL command to nt.sqlite"""
    cur = con.cursor()

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
