#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 14:24:59 2020

@author: shane
"""

import csv


def parse_parameters(nutra_dir):
    parameters = {}
    with open(f"{nutra_dir}/parameters.csv") as f:
        # TODO: filter '#' comment lines
        csv_reader = csv.reader(f)
        rows = list(csv_reader)[1:]
        for row in rows:
            name = row[0]
            value = row[1]
            if name and value:
                parameters[name] = value
    return parameters
