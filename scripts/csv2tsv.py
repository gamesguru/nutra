#!/usr/bin/env python3
import sys
import csv
import os

# run this out a directory with multiple *.csv files, it will output tab-delimited *.txt files

for ogfile in os.listdir(os.getcwd()):
    if ogfile.endswith('.csv'):
        with open(ogfile) as f:
            with open(ogfile.replace('.csv', '.txt'), 'w+') as newfile:
                for row in csv.reader(f):
                    newfile.write('\t'.join(row) + '\n')
