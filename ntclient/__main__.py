# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 16:02:19 2020

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutrient analysis and composition application.
Copyright (C) 2018-2020  Shane Jaroch

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import sys
import traceback

from colorama import init as colorama_init

# Check Python version
if sys.version_info < (3, 6, 5):
    ver = ".".join([str(x) for x in sys.version_info[0:3]])
    print("ERROR: nutra requires Python 3.6.5 or later to run")
    print("HINT:  You're running Python " + ver)
    exit(1)
else:
    from . import __dbver__, __sha__, __title__, __version__

    # from .account import cmd_login
    from .parsers import analyze, day, nutrients, search, sort
    from .utils.settings import TESTING, VERBOSITY

    colorama_init()  # colorama

# TODO:
# - display full food name in results
# - display refuse
# - function to list out nutrients and info on them
# - sort function
# - nested nutrient tree, like: http://www.whfoods.com/genpage.php?tname=nutrientprofile&dbid=132


def build_argparser():
    # global login_parser

    arg_parser = argparse.ArgumentParser(prog=__title__)
    arg_parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{__title__} version "
        + f"{__version__}   ({__sha__})  [DB v{__dbver__}]",
    )

    # --------------------------
    # Sub-command parsers
    # --------------------------
    subparsers = arg_parser.add_subparsers(
        title="nutra subcommands",
        description="valid subcommands",
        help="additional help",
    )

    # TODO: init subcommand to onboard db and parameters.csv in ~/.nutra ??

    # Search subcommand
    search_parser = subparsers.add_parser(
        "search", help="use to search foods and recipes"
    )
    search_parser.add_argument(
        "terms",
        type=str,
        nargs="+",
        help='search query, e.g. "grass fed beef" or "ultraviolet mushrooms"',
    )
    search_parser.set_defaults(func=search)

    # Sort subcommand
    sort_parser = subparsers.add_parser("sort", help="use to sort foods by nutrient ID")
    sort_parser.add_argument(
        "--kcal",
        "-c",
        action="store_true",
        help="sort by value per 200 kcal, instead of per 100 g",
    )
    sort_parser.add_argument("nutr_id", type=int)
    sort_parser.set_defaults(func=sort)

    # Analyze subcommand
    analyze_parser = subparsers.add_parser(
        "anl", help="use to analyze foods, recipes, logs"
    )
    analyze_parser.add_argument("food_id", type=int, nargs="+")
    analyze_parser.set_defaults(func=analyze)

    # Day (analyze-day) subcommand
    day_parser = subparsers.add_parser("day", help="use to sort foods by nutrient ID")
    day_parser.add_argument(
        "food_log", type=str, nargs="+", help="path to CSV file of food log"
    )
    day_parser.add_argument(
        "--rda", "-r", help="provide a custom RDA file in csv format",
    )
    day_parser.set_defaults(func=day)

    # Nutrient subcommand
    nutrient_parser = subparsers.add_parser(
        "nt", help="list out nutrients and their info"
    )
    nutrient_parser.set_defaults(func=nutrients)

    # # Login subcommand
    # login_parser = subparsers.add_parser("login", help="log in to your account")
    # login_parser.set_defaults(func=cmd_login)

    return arg_parser


def main(argv=None):
    if argv is None:
        argv = sys.argv
    arg_parser = build_argparser()
    # Used for testing
    if TESTING and len(sys.argv) < 2:
        # --------------------------------
        # sys.argv = [
        #     "./nutra",
        #     "day",
        #     "~/.nutra/rocky.csv",
        #     # "~/.nutra/rocky-mom.csv",
        #     "-r",
        #     "~/.nutra/dog-rdas-18lbs.csv",
        # ]
        # --------------------------------
        # sys.argv = [
        #     "./nutra",
        #     "day",
        #     "~/.nutra/rocky.csv",
        # ]
        # --------------------------------
        # sys.argv = [
        #     "./nutra",
        #     "day",
        #     "resources/dog-simple.csv",
        #     "-r",
        #     "resources/dog-rdas-18lbs.csv",
        # ]
        # --------------------------------
        # sys.argv = ["./nutra"]
        # sys.argv = ["./nutra", "sort"]
        # sys.argv = ["./nutra", "sort", "789"]
        # sys.argv = ["./nutra", "sort", "-c", "789"]
        # sys.argv = ["./nutra", "anl", "9050", "9052"]
        # sys.argv = ["./nutra", "nt"]
        sys.argv = ["./nutra", "search", "grass", "fed", "beef"]
        # sys.argv = ["./nutra", "search", "grass"]
    try:
        args = arg_parser.parse_args()
        # args, unknown = arg_parser.parse_known_args()
        if hasattr(args, "func"):
            subparsers_actions = [
                action
                for action in arg_parser._actions
                if isinstance(action, argparse._SubParsersAction)
            ]
            subparsers = subparsers_actions[0].choices
            ######################
            # Run the cmd function
            args.func(args, arg_parser=arg_parser, subparsers=subparsers)
        else:
            arg_parser.print_help()
    except Exception as e:
        print("There was an unforseen error: ", repr(e))
        if TESTING or VERBOSITY > 0:
            trace = "\n".join(traceback.format_tb(e.__traceback__))
            print(trace)
        arg_parser.print_help()
