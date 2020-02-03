# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:09:07 2019

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutraent analysis and composition application.
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

import os

from dotenv import load_dotenv

# Read in .env file if it exists locally, else look to env vars
load_dotenv()

NUTRA_DIR = os.path.join(os.path.expanduser("~"), ".nutra")

REMOTE_HOST = "https://nutra-server.herokuapp.com"
SERVER_HOST = os.getenv("NUTRA_OVERRIDE_LOCAL_SERVER_HOST", REMOTE_HOST)

TESTING = SERVER_HOST != REMOTE_HOST
