from tabulate import tabulate

from ..utils.sqlfuncs.nt import (
    conn,
    sql_biometric_add,
    sql_biometric_logs,
    sql_biometrics,
)


def biometrics():
    headers, rows = sql_biometrics()
    table = tabulate(rows, headers=headers, tablefmt="presto")
    print(table)
    return rows


def biometric_logs():
    profile_id = 1  # TODO: current profile
    headers, rows = sql_biometric_logs(profile_id)

    table = tabulate(rows, headers=headers, tablefmt="presto")
    print(table)
    return rows


def biometric_add(bio_vals):
    print()
    # print("New biometric log: " + name + "\n")

    cur = conn.cursor()
    bio_names = {x[0]: x for x in sql_biometrics()}

    results = []
    for id, value in bio_vals.items():
        bio = bio_names[id]
        results.append({"id": id, "name": bio[1], "value": value, "unit": bio[2]})

    table = tabulate(results, headers="keys", tablefmt="presto")
    print(table)

    # TODO: print current profile and date?

    confirm = input("\nConfirm add biometric? [Y/n] ")

    if confirm.lower() == "y":
        sql_biometric_add(bio_vals)
        print("not implemented ;]")
