#!/usr/bin/env python3
import sys

file = sys.argv[1]

import csv

n = 0
with open(file, "r") as source:
    rdr = csv.reader(source)
    for row in csv.reader(source):
        n = len(row)
        print(f'{n} rows')
        break

for i in range(0, n):
    longest = 0
    with open(file, "r") as source:
        rdr = csv.reader(source)
        for j, row in enumerate(rdr):
            e = row[i]
            if j == 0:
                print(f'\n\n\n{e}')
                continue
            if len(e) > longest:
                # print(e)
                longest = len(e)
                print(f'{longest}')
