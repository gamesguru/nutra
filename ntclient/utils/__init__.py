# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:09:07 2019

@author: shane
"""

import os

from colorama import Fore
from dotenv import load_dotenv

from .gitutils import git_sha
from .csvutils import parse_parameters
from .sqlfuncs import __dbversion__, __dbtarget__


# Export for package level
__sha__ = git_sha()
__dbversion__ = __dbversion__
__dbtarget__ = __dbtarget__

# Read in .env file if it exists locally, else look to env vars
load_dotenv(verbose=False)

NUTRA_DIR = os.path.join(os.path.expanduser("~"), ".nutra")
try:
    parameters = parse_parameters(NUTRA_DIR)
except Exception as e:
    print(f"Warning: {repr(e)} ['~/.nutra/parameters.csv']")
    parameters = dict()


TESTING = bool(int(os.getenv("NUTRA_CLI_NO_ARGS_INJECT_MOCKS", False)))
# TODO: support more settings via parameters.csv
VERBOSITY = 1


# ---------------------------
# Colors and other settings
# ---------------------------

THRESH_WARN = 0.7
COLOR_WARN = Fore.YELLOW

THRESH_CRIT = 0.4
COLOR_CRIT = Fore.RED

THRESH_OVER = 1.9
# COLOR_OVER = Fore.LIGHTBLACK_EX
COLOR_OVER = Fore.LIGHTMAGENTA_EX

COLOR_DEFAULT = Fore.BLUE

SEARCH_LIMIT = 150
FOOD_NAME_TRUNC = (
    int(parameters["FOOD_NAME_TRUNC"]) if "FOOD_NAME_TRUNC" in parameters else 200
)


# ------------------------
# Nutrient IDs
# ------------------------
NUTR_ID_KCAL = 208

NUTR_ID_PROTEIN = 203

NUTR_ID_CARBS = 205
NUTR_ID_SUGAR = 269
NUTR_ID_FIBER = 291

NUTR_ID_FAT_TOT = 204
NUTR_ID_FAT_SAT = 606
NUTR_ID_FAT_MONO = 645
NUTR_ID_FAT_POLY = 646


NUTR_IDS_FLAVONES = [
    710,
    711,
    712,
    713,
    714,
    715,
    716,
    734,
    735,
    736,
    737,
    738,
    731,
    740,
    741,
    742,
    743,
    745,
    749,
    750,
    751,
    752,
    753,
    755,
    756,
    758,
    759,
    762,
    770,
    773,
    785,
    786,
    788,
    789,
    791,
    792,
    793,
    794,
]

NUTR_IDS_AMINOS = [
    501,
    502,
    503,
    504,
    505,
    506,
    507,
    508,
    509,
    510,
    511,
    512,
    513,
    514,
    515,
    516,
    517,
    518,
    521,
]
