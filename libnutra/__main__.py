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

from . import __version__

# Check Python version
if sys.version_info < (3, 6, 5):
    ver = ".".join([str(x) for x in sys.version_info[0:3]])
    print(
        "ERROR: nutra requires Python 3.6.5 or later to run",
        f"HINT:  You're running Python {ver}",
        sep="\n",
    )
    exit(1)


def build_argparser():

    usage = """
    An extensible food database to analyze recipes and aid in fitness.
    Version {__version__}

    Usage: %(prog)s [options] <command> [options]
    """

    arg_parser = argparse.ArgumentParser(prog="nutra", usage=usage)

    arg_parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )

    arg_parser.add_argument(
        "--key",
        dest="key",
        metavar="KEY",
        default=None,
        help="set the secret key to sign with",
    )

    arg_parser.add_argument(
        "--alg",
        dest="algorithm",
        metavar="ALG",
        default="HS256",
        help="set crypto algorithm to sign with. default=HS256",
    )

    subparsers = arg_parser.add_subparsers(
        title="PyJWT subcommands",
        description="valid subcommands",
        help="additional help",
    )

    # Encode subcommand
    encode_parser = subparsers.add_parser(
        "encode", help="use to encode a supplied payload"
    )

    payload_help = """Payload to encode. Must be a space separated list of key/value
    pairs separated by equals (=) sign."""

    encode_parser.add_argument("payload", nargs="+", help=payload_help)
    encode_parser.set_defaults(func=encode_payload)

    # Decode subcommand
    decode_parser = subparsers.add_parser(
        "decode", help="use to decode a supplied JSON web token"
    )
    decode_parser.add_argument("token", help="JSON web token to decode.", nargs="?")

    decode_parser.add_argument(
        "-n",
        "--no-verify",
        action="store_false",
        dest="verify",
        default=True,
        help="ignore signature and claims verification on decode",
    )

    decode_parser.set_defaults(func=decode_payload)

    return arg_parser


def main(args):
    arg_parser = build_argparser()

    try:
        arguments = arg_parser.parse_args(args)
        output = arguments.func(arguments)
        print(output)
    except Exception as e:
        print("There was an unforseen error: ", e)
        arg_parser.print_help()
