from ..utils.sqlfuncs.nt import (
    biometric_add as _biometric_add,
    biometric_logs,
    biometrics as _biometrics,
    conn,
)

from tabulate import tabulate


def biometrics():
    # TODO: current profile
    profile_id = 1
    headers, log_rows = biometric_logs(profile_id)

    table = tabulate(log_rows, headers=headers, tablefmt="presto")
    print(table)


def biometric_add(bio_vals):
    print()
    # print("New biometric log: " + name + "\n")

    cur = conn.cursor()
    bio_names = {x[0]: x for x in _biometrics()}

    results = []
    for id, value in bio_vals.items():
        bio = bio_names[id]
        results.append({"id": id, "name": bio[1], "value": value, "unit": bio[2]})

    table = tabulate(results, headers="keys", tablefmt="presto")
    print(table)

    # TODO: print current profile and date?

    confirm = input("\nConfirm add biometric? [Y/n] ")

    if confirm.lower() == "y":
        _biometric_add(bio_vals)
        print("not implemented ;]")
