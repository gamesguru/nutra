# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 16:01:31 2020

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


def git_sha():
    """ Gets the git revision, if it exists in cwd """
    try:
        sha = open("git-rev").read().rstrip()
    except Exception as e1:
        print(e1)
        import subprocess

        try:
            sha = (
                subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
                .decode()
                .rstrip()
            )
        except Exception as e2:
            print(e2)
            sha = None

    return sha


##################
# Standard details
__title__ = "nutra"
__version__ = "0.0.24"
__sha__ = git_sha()
__author__ = "Shane Jaroch"
__license__ = "GPL v3"
__copyright__ = "Copyright 2018-2020 Shane Jaroch"
