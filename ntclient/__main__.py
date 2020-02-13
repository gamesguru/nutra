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

# Check Python version
if sys.version_info < (3, 6, 5):
    ver = ".".join([str(x) for x in sys.version_info[0:3]])
    print("ERROR: nutra requires Python 3.6.5 or later to run")
    print("HINT:  You're running Python " + ver)
    exit(1)

from . import __version__
from .account import cmd_login
from .analyze import cmd_analyze
from .search import cmd_search
from .utils.settings import TESTING


def build_argparser():
    global login_parser

    arg_parser = argparse.ArgumentParser(prog="nutra")
    arg_parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
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

    # Analyze subcommand
    analyze_parser = subparsers.add_parser(
        "anl", help="use to analyze foods, recipes, logs"
    )
    analyze_parser.add_argument("-r", help="recipe ID", type=int)
    # analyze_parser.add_argument("token", help="JSON web token to decode.", nargs="?")
    analyze_parser.set_defaults(func=cmd_analyze)  # , nargs="+")

    # Login subcommand
    login_parser = subparsers.add_parser("login", help="log in to your account")
    login_parser.set_defaults(func=cmd_login)

    return arg_parser


def main(argv=None):
    if argv == None:
        argv = sys.argv
    arg_parser = build_argparser()
    # Used for testing
    if TESTING and len(sys.argv) < 2:
        sys.argv = ["./nutra", "anl", "1001"]
        # sys.argv = ["./nutra", "search", "grass", "fed", "beef"]
    try:
        args, unknown = arg_parser.parse_known_args()
        args.func(args, unknown, arg_parser=arg_parser)
    except Exception as e:
        # print_tb(e)
        print("There was an unforseen error: ", e)
        arg_parser.print_help()
