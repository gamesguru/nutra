#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:16:08 2020

@author: shane
"""

from tabulate import tabulate

from .utils import remote


def list_nutrients():
    response = remote.request("/nutrients")
    results = response.json()["data"]

    table = tabulate(results, headers="keys", tablefmt="presto")
    print(table)
