from ..utils.sqlfuncs.nt import biometric_add as _biometric_add, biometrics

from tabulate import tabulate


def biometric_add(bio_vals):
    print()
    # print("New biometric log: " + name + "\n")

    bio_names = {x[0]: x for x in biometrics()}

    results = []
    for id, value in bio_vals.items():
        bio = bio_names[id]
        results.append({"id": id, "name": bio[1], "value": value, "unit": bio[2]})

    table = tabulate(results, headers="keys", tablefmt="presto")
    print(table)

    # TODO: print current user and date?

    confirm = input("\nConfirm add biometric? [Y/n] ")

    if confirm.lower() == "y":
        _biometric_add(bio_vals)
        print("not implemented ;]")
