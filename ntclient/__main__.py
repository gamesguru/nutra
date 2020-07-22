# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 16:02:19 2020

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutrient analysis and composition application.
Copyright (C) 2018  Shane Jaroch

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

# Check Python version
if sys.version_info < (3, 6, 5):
    ver = ".".join([str(x) for x in sys.version_info[0:3]])
    print("ERROR: nutra requires Python 3.6.5 or later to run")
    print("HINT:  You're running Python " + ver)
    exit(1)
else:
    from . import __sha__, __title__, __version__

    # from .account import cmd_login
    from .analyze import cmd_analyze
    from .parsers import day, nutrients, sort
    from .search import cmd_search
    from .utils.settings import TESTING

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
        version=f"{__title__} version " + f"{__version__}   ({__sha__})",
    )

    # --------------------------
    # Sub-command parsers
    # --------------------------
    subparsers = arg_parser.add_subparsers(
        title="nutra subcommands",
        description="valid subcommands",
        help="additional help",
    )

    # Search subcommand
    search_parser = subparsers.add_parser(
        "search", help="use to search foods and recipes"
    )
    search_parser.set_defaults(func=cmd_search, nargs="+")

    # Sort subcommand
    sort_parser = subparsers.add_parser("sort", help="use to sort foods by nutrient ID")
    sort_parser.set_defaults(func=sort, nargs="+")

    # Analyze subcommand
    analyze_parser = subparsers.add_parser(
        "anl", help="use to analyze foods, recipes, logs"
    )
    analyze_parser.add_argument("-r", help="recipe ID", type=int)
    # analyze_parser.add_argument("token", help="JSON web token to decode.", nargs="?")
    analyze_parser.set_defaults(func=cmd_analyze)  # , nargs="+")

    # Day (analyze-day) subcommand
    day_parser = subparsers.add_parser("day", help="use to sort foods by nutrient ID")
    day_parser.set_defaults(func=day, nargs="+")

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
        sys.argv = [
            "./nutra",
            "day",
            "~/.nutra/rocky.csv",
            "~/.nutra/dog-rdas-18lbs.csv",
        ]
        # sys.argv = ["./nutra", "sort", "789"]
        # sys.argv = ["./nutra", "anl", "11233"]
        # sys.argv = ["./nutra", "nt"]
        # sys.argv = ["./nutra", "search", "grass", "fed", "beef"]
    try:
        args, unknown = arg_parser.parse_known_args()
        args.func(args, unknown, arg_parser=arg_parser)
    except Exception as e:
        print("There was an unforseen error: ", repr(e))
        if TESTING:
            trace = "\n".join(traceback.format_tb(e.__traceback__))
            print(trace)
        arg_parser.print_help()
