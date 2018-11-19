#!/usr/bin/env python3
import sys
import os

# removes given column indicies, get rid of those schemas
# e.g. to remove the 4th column: `./tsv_strip_columns.py  Nutrient.txt 3`

file = sys.argv[1]
indicies = sys.argv[2].split(',')

with open(file, 'r') as f:
    with open(f'adj_{file}', 'w+') as f2:
        for line in f.readlines():
            els = line.rstrip().split('\t')
            newels = []
            for i, el in enumerate(els):
                if not str(i) in indicies:
                    newels.append(el)
            f2.write('\t'.join(newels) + '\n')
