#!/usr/bin/env python3
import sys

file = sys.argv[1]
indicies = sys.argv[2].split(',')

import csv
with open(file, "r") as source:
    rdr = csv.reader(source)
    with open(file + '-processed', "w+") as result:
        wtr = csv.writer(result)
        for r in rdr:
            row = []
            for i in indicies:
                row.append(r[int(i) - 1])
            wtr.writerow(row)
