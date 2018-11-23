#!/usr/bin/env python3
import sys
import csv
import os

# run this out a directory with multiple *.csv files, it will output tab-delimited *.txt files
_encoding = 'iso-8859-1'

for ogfile in os.listdir(os.getcwd()):
    print(ogfile + '\n')
    if ogfile.endswith('.csv'):
        with open(ogfile, encoding=_encoding) as f:
            with open(ogfile.replace('.csv', '.txt'), 'w+', encoding='utf-8') as newfile:
                for row in csv.reader(f):
                    newfile.write('\t'.join(row) + '\n')
